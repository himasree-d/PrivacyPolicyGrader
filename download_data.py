#!/usr/bin/env python3
"""
download_data.py — Downloads and caches privacy policy data.

Usage:
    python download_data.py           # Download all default URLs
    python download_data.py --url <U> # Download a single URL

Satisfies: "No data/ with a download script — just cached JSON results."
This script creates data/<name>_data.json for each site.
"""

import os
import sys
import json
import logging
import argparse

from src.scraper import PolicyScraper
from src.preprocess import TextPreprocessor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

DEFAULT_SITES = [
    {"name": "Google",       "url": "https://policies.google.com/privacy"},
    {"name": "Instagram",    "url": "https://help.instagram.com/519522125107875"},
    {"name": "FreeCodeCamp", "url": "https://www.freecodecamp.org/news/privacy-policy/"},
]


def download_and_cache(url: str, name: str) -> bool:
    """Scrapes URL, preprocesses, and saves to data/<name>_data.json."""
    scraper = PolicyScraper()
    preprocessor = TextPreprocessor()

    logger.info(f"Downloading: {name} — {url}")
    raw_text = scraper.scrape(url)
    if not raw_text:
        logger.error(f"Failed to download {name}")
        return False

    cleaned = preprocessor.clean_text(raw_text)
    chunks = preprocessor.chunk_text(cleaned)

    payload = {
        "name": name,
        "url": url,
        "num_chunks": len(chunks),
        "raw_length": len(raw_text),
        "chunks": chunks,
    }
    filename = f"{name.lower().replace(' ', '_')}_data.json"
    preprocessor.save_processed(payload, filename)
    logger.info(f"  Saved {len(chunks)} chunks → data/{filename}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Download privacy policy data")
    parser.add_argument("--url",  type=str, help="URL to download")
    parser.add_argument("--name", type=str, default="custom")
    args = parser.parse_args()

    os.makedirs("data", exist_ok=True)

    if args.url:
        ok = download_and_cache(args.url, args.name)
        sys.exit(0 if ok else 1)

    success = 0
    for site in DEFAULT_SITES:
        if download_and_cache(site["url"], site["name"]):
            success += 1

    logger.info(f"\nDownloaded {success}/{len(DEFAULT_SITES)} sites.")
    logger.info("Run `python pipeline.py` next to analyze and grade.")


if __name__ == "__main__":
    main()
