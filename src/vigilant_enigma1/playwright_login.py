import json
import os
from pathlib import Path
from typing import Optional
from playwright.sync_api import sync_playwright

DEFAULT_UA = os.getenv("USER_AGENT","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36")

def _maybe_stealth(page) -> None:
    try:
        from playwright_stealth import stealth_sync  # type: ignore
        stealth_sync(page)
    except Exception:
        pass

def login_and_get_html(username: str, password: str, target_url: str, headless: bool = True, proxy: Optional[str] = None, storage_dir: str = ".playwright") -> str:
    storage = Path(storage_dir); storage.mkdir(parents=True, exist_ok=True)
    state_path = storage / "state.json"
    launch_kwargs: dict = {"headless": headless}
    if proxy: launch_kwargs["proxy"] = {"server": proxy}
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs)
        context = browser.new_context(storage_state=str(state_path) if state_path.exists() else None, user_agent=DEFAULT_UA)
        page = context.new_page(); _maybe_stealth(page)
        page.goto("https://www.instagram.com/", wait_until="networkidle")
        needs_login = page.locator('input[name="username"]').count() > 0
        if needs_login:
            if not username or not password: browser.close(); raise ValueError("需要 IG_USERNAME/IG_PASSWORD")
            page.fill('input[name="username"]', username); page.fill('input[name="password"]', password)
            page.click('button[type="submit"]'); page.wait_for_load_state("networkidle", timeout=60000)
            for txt in ("Not Now","稍后再说"):
                try: page.get_by_text(txt, exact=True).click(timeout=3000)
                except Exception: pass
            context.storage_state(path=str(state_path))
        page.goto(target_url, wait_until="networkidle")
        html = page.content(); context.storage_state(path=str(state_path)); browser.close()
        return html

def export_cookies(storage_dir: str = ".playwright") -> list[dict]:
    state_path = Path(storage_dir) / "state.json"
    if not state_path.exists(): return []
    data = json.loads(state_path.read_text(encoding="utf-8"))
    return data.get("cookies", [])
