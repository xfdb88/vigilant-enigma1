from __future__ import annotations

import argparse
import asyncio
import os
from typing import List

from dotenv import load_dotenv
from .scraper import scrape_urls, write_csv
from .logger import init_logger

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="scrape", description="Minimal async scraper")
    p.add_argument("--url", help="单个 URL")
    p.add_argument("--infile", help="包含 URL 列表的文本文件，每行一个")
    p.add_argument("--out", default="output.csv", help="输出 CSV 路径，默认 output.csv")
    p.add_argument("--browser", action="store_true", help="使用 Playwright（需要安装 extras 'browser'）")
    p.add_argument("--concurrency", type=int, default=int(os.getenv("CONCURRENCY", "5")), help="并发数")
    return p.parse_args()

def main() -> None:
    load_dotenv()
    logger = init_logger()
    args = parse_args()

    urls: List[str] = []
    if args.url:
        urls.append(args.url)
    if args.infile:
        with open(args.infile, "r", encoding="utf-8") as f:
            urls.extend([line.strip() for line in f if line.strip()])

    if not urls:
        logger.warning("未提供 URL。使用 --url 或 --infile。")
        return
    logger.info("开始抓取，共 %d 个 URL", len(urls))
    results = asyncio.run(scrape_urls(urls, use_browser=args.browser, concurrency=args.concurrency))
    write_csv(results, args.out)
    logger.info("完成，已写出 %s", args.out)
