from __future__ import annotations

import asyncio
import csv
import os
import time
from contextlib import asynccontextmanager
from typing import Any, Dict, Iterable, List, Optional

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from tqdm import tqdm
from .ratelimiter import AsyncRateLimiter
from .config import Config
from .logger import init_logger
from .ratelimiter import RateLimiter
from .playwright_login import login_and_get_html, export_cookies
from .parser import parse_profile

DEFAULT_UA = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
)
# 读取可配置参数（带默认）
PROXY_URL = (os.getenv("PROXY_URL") or "").strip() or None
HEADLESS = (os.getenv("HEADLESS", "true").lower() in ("1", "true", "yes", "on"))
RATE_LIMIT_QPS = float(os.getenv("RATE_LIMIT_QPS", "0") or 0)
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3") or 3)
RETRY_BACKOFF = float(os.getenv("RETRY_BACKOFF", "2") or 2.0)
DEFAULT_TIMEOUT = float(os.getenv("TIMEOUT_SECONDS", os.getenv("TIMEOUT", "15")) or 15)

def _try_import(name: str):
    try:
        __import__(name)
        return True
    except Exception:
        return False

@asynccontextmanager
async def _async_client(timeout: float = DEFAULT_TIMEOUT, ua: str = DEFAULT_UA):
    headers = {"User-Agent": ua, "Accept": "text/html,application/xhtml+xml"}
    # 加载代理（如有）
    client_kwargs = dict(
        headers=headers,
        timeout=httpx.Timeout(timeout, read=timeout),
        follow_redirects=True,
        http2=True,
    )
    if PROXY_URL:
        client_kwargs["proxies"] = PROXY_URL  # type: ignore[assignment]
    async with httpx.AsyncClient(**client_kwargs) as client:
        yield client

# 使用可配置的重试策略
@retry(
    stop=stop_after_attempt(RETRY_ATTEMPTS),
    wait=wait_exponential(multiplier=RETRY_BACKOFF, min=RETRY_BACKOFF, max=RETRY_BACKOFF * 8),
    retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
    reraise=True,
)
async def fetch_httpx(client: httpx.AsyncClient, url: str) -> str:
    resp = await client.get(url)
    resp.raise_for_status()
    return resp.text

async def fetch_browser(url: str, timeout: float = DEFAULT_TIMEOUT) -> str:
    try:
        from playwright.async_api import async_playwright
    except ImportError as e:
        raise RuntimeError("Playwright 未安装，请安装 extras 'browser' 后使用 --browser") from e

    async with async_playwright() as p:
        launch_kwargs = {"headless": HEADLESS}
        if PROXY_URL:
            launch_kwargs["proxy"] = {"server": PROXY_URL}
        browser = await p.chromium.launch(**launch_kwargs)
        context = await browser.new_context(user_agent=DEFAULT_UA)
        page = await context.new_page()
        # 可选 stealth
        if _try_import("playwright_stealth"):
            from playwright_stealth import stealth_async
            await stealth_async(page)
        await page.goto(url, wait_until="domcontentloaded", timeout=int(timeout * 1000))
        content = await page.content()
        await browser.close()
        return content

def parse_html(html: str, url: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "lxml")
    title = (soup.title.string or "").strip() if soup.title and soup.title.string else ""
    desc = ""
    mt = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    if mt and mt.get("content"):
        desc = mt["content"].strip()
    return {"url": url, "title": title, "description": desc}

async def _worker(url: str, use_browser: bool, client: Optional[httpx.AsyncClient]) -> Dict[str, Any]:
    html = await (fetch_browser(url) if use_browser else fetch_httpx(client, url))  # type: ignore[arg-type]
    return parse_html(html, url)

async def scrape_urls(urls: Iterable[str], use_browser: bool = False, concurrency: int = 5) -> List[Dict[str, Any]]:
    semaphore = asyncio.Semaphore(concurrency)
    results: List[Dict[str, Any]] = []

    # 用异步限速器统一控制 QPS
    limiter = AsyncRateLimiter(RATE_LIMIT_QPS)

    async with _async_client(timeout=DEFAULT_TIMEOUT) as client:
        async def limited(u: str):
            async with semaphore:
                await limiter.wait()
                return await _worker(u, use_browser, client)

        tasks = [limited(u) for u in urls]
        for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="scraping"):
            try:
                res = await coro
                results.append(res)
            except Exception as e:
                results.append({"url": "...", "title": "", "description": f"ERROR: {e}"})
        return results

def write_csv(rows: List[Dict[str, Any]], out_path: str) -> None:
    if not rows:
        return
    # 若已安装 pandas，则优先使用
    try:
        import pandas as pd  # type: ignore
        df = pd.DataFrame(rows)
        df.to_csv(out_path, index=False)
        return
    except Exception:
        pass

    keys = list(rows[0].keys())
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)

class TransientError(Exception): pass


def read_usernames(path: str) -> List[str]:
    users: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            u = (row.get("username") or "").strip().lstrip("@")
            if u: users.append(u)
    return users


def write_rows(path: str, rows: List[Dict]):
    need_header = not Path(path).exists()
    with open(path, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["username","display_name","bio","email","phone","links","gender","age","region","warning_code","error"])
        if need_header: w.writeheader()
        for r in rows: w.writerow(r)


def build_profile_url(username: str) -> str: return f"https://www.instagram.com/{username}/"


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(TransientError),
    reraise=True,
)
def fetch_html_with_playwright(cfg: Config, url: str) -> str:
    try: return login_and_get_html(cfg.ig_user, cfg.ig_pass, url, headless=cfg.headless, proxy=cfg.proxy)
    except Exception as e: raise TransientError(str(e))


def cookies_to_jar(cookies: List[dict]) -> httpx.Cookies:
    jar = httpx.Cookies()
    for c in cookies:
        name, value = c.get("name"), c.get("value")
        if name is None or value is None: continue
        jar.set(name, value, domain=c.get("domain") or None, path=c.get("path") or "/")
    return jar


def fetch_html_with_httpx(cfg: Config, url: str) -> str:
    """
    使用 httpx 抓取示例：从 Playwright 持久化的 storageState 导出 cookies 并复用。
    注意：Instagram 对无头与反爬较严格，httpx 成功率可能低于 Playwright。
    """
    cookies = export_cookies(); jar = cookies_to_jar(cookies)
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml"}
    kwargs = dict(headers=headers, cookies=jar, timeout=httpx.Timeout(cfg.timeout, read=cfg.timeout), follow_redirects=True, http2=True)
    if cfg.proxy: kwargs["proxies"] = cfg.proxy  # type: ignore[assignment]
    with httpx.Client(**kwargs) as client:
        r = client.get(url); r.raise_for_status(); return r.text


def scrape(cfg: Config, input_csv: str, output_csv: str, use_httpx: bool = False):
    logger = init_logger("igscraper")
    usernames = read_usernames(input_csv)
    if not usernames: logger.warning("输入为空或未找到 username 列"); return
    limiter = RateLimiter(cfg.qps); rows_out: List[Dict] = []
    for u in usernames:
        limiter.wait()
        url = build_profile_url(u); logger.info("抓取 %s -> %s", u, url)
        try:
            html = fetch_html_with_httpx(cfg, url) if use_httpx else fetch_html_with_playwright(cfg, url)
            row, _ = parse_profile(html, u)
        except Exception as e:
            row = {"username":u,"display_name":"","bio":"","email":"","phone":"","links":"","gender":"","age":"","region":"","warning_code":"","error":f"{type(e).__name__}: {e}"}
            logger.error("%s 报错: %s", u, row["error"])
        rows_out.append(row)
        if len(rows_out) >= 20: write_rows(output_csv, rows_out); rows_out.clear()
    if rows_out: write_rows(output_csv, rows_out)
