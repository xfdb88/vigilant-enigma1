from __future__ import annotations

import asyncio
import csv
import os
from contextlib import asynccontextmanager
from typing import Any, Dict, Iterable, List, Optional

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from tqdm import tqdm

DEFAULT_UA = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
)
DEFAULT_TIMEOUT = float(os.getenv("TIMEOUT", "15"))

def _try_import(name: str):
    try:
        __import__(name)
        return True
    except Exception:
        return False

@asynccontextmanager
async def _async_client(timeout: float = DEFAULT_TIMEOUT, ua: str = DEFAULT_UA):
    headers = {"User-Agent": ua, "Accept": "text/html,application/xhtml+xml"}
    async with httpx.AsyncClient(
        headers=headers,
        timeout=httpx.Timeout(timeout, read=timeout),
        follow_redirects=True,
        http2=True,
    ) as client:
        yield client

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
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
        browser = await p.chromium.launch(headless=True)
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

    async with _async_client() as client:
        async def limited(u: str):
            async with semaphore:
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
