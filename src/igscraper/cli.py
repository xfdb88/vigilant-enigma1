from __future__ import annotations

import argparse
from dotenv import load_dotenv

from vigilant_enigma1.config import Config
from vigilant_enigma1.logger import init_logger
from vigilant_enigma1.scraper import scrape as run_scrape

def main() -> None:
    load_dotenv()
    p = argparse.ArgumentParser(prog="igscrape", description="Instagram public profile scraper")
    p.add_argument("-i","--input", default="data/input.csv", help="输入 CSV（需包含 username 列）")
    p.add_argument("-o","--output", default="data/output.csv", help="输出 CSV")
    p.add_argument("--httpx", action="store_true", help="使用 httpx+Cookies 抓取（默认 Playwright）")
    args = p.parse_args()
    logger = init_logger("igscraper")
    cfg = Config()
    logger.info("开始：input=%s output=%s httpx=%s qps=%.3f", args.input, args.output, args.httpx, cfg.qps)
    run_scrape(cfg, args.input, args.output, use_httpx=args.httpx)
    logger.info("完成")
