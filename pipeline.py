#!/usr/bin/env python3
"""
pipeline.py — Runnable end-to-end data pipeline for Privacy Policy Grader.

Usage:
    python pipeline.py                          # Run all default URLs
    python pipeline.py --url <URL> --name <X>  # Run single URL
    python pipeline.py --text "paste policy"   # Run from raw text

This script satisfies the requirement:
  "Pipelines must be runnable scripts, not only notebooks."
"""

import os
import sys
import json
import logging
import argparse
from dotenv import load_dotenv

from src.scraper import PolicyScraper
from src.preprocess import TextPreprocessor
from src.model import PolicyAnalyzer
from src.grader import PolicyGrader

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("pipeline.log"),
    ]
)
logger = logging.getLogger(__name__)

DEFAULT_SITES = [
    {"name": "Google",     "url": "https://policies.google.com/privacy"},
    {"name": "Instagram",  "url": "https://help.instagram.com/519522125107875"},
    {"name": "FreeCodeCamp", "url": "https://www.freecodecamp.org/news/privacy-policy/"},
]


def run_pipeline(url_or_text: str, name: str = "sample") -> dict | None:
    """
    Full pipeline: ingest → preprocess → model → grade → save.
    Returns the final graded result dict, or None on failure.
    """
    logger.info(f"=== Pipeline start: {name} ===")

    # 1. Ingestion
    scraper = PolicyScraper()
    if url_or_text.startswith("http"):
        raw_text = scraper.scrape(url_or_text)
    else:
        raw_text = url_or_text
        logger.info("Using raw text input (no scraping needed).")

    if not raw_text:
        logger.error("Ingestion failed — no text returned.")
        return None

    # 2. Preprocessing
    preprocessor = TextPreprocessor()
    cleaned_text = preprocessor.clean_text(raw_text)
    chunks = preprocessor.chunk_text(cleaned_text)

    # Save processed data to data/ folder
    processed_payload = {
        "name": name,
        "source": url_or_text if url_or_text.startswith("http") else "<raw_text>",
        "num_chunks": len(chunks),
        "chunks": chunks,
    }
    data_filename = f"{name.lower().replace(' ', '_')}_data.json"
    preprocessor.save_processed(processed_payload, data_filename)
    logger.info(f"Processed data saved → data/{data_filename}")

    # 3. Model analysis
    analyzer = PolicyAnalyzer()
    extracted_data = analyzer.analyze_chunks(chunks)

    # 4. Grading
    grader = PolicyGrader()
    final_results = grader.process(extracted_data)
    final_results["name"] = name

    # 5. Persist results
    os.makedirs("results", exist_ok=True)
    output_filename = f"{name.lower().replace(' ', '_')}_results.json"
    output_path = os.path.join("results", output_filename)
    with open(output_path, "w") as f:
        json.dump(final_results, f, indent=4)
    logger.info(f"Results saved → {output_path}")

    logger.info(f"=== Pipeline done: {name} | Grade={final_results.get('grade')} | Score={final_results.get('final_risk_score')} ===")
    return final_results


def main():
    parser = argparse.ArgumentParser(description="Privacy Policy Grader Pipeline")
    parser.add_argument("--url",  type=str, help="Single URL to analyze")
    parser.add_argument("--text", type=str, help="Raw policy text to analyze")
    parser.add_argument("--name", type=str, default="custom", help="Name for this run")
    args = parser.parse_args()

    if args.url:
        result = run_pipeline(args.url, args.name)
    elif args.text:
        result = run_pipeline(args.text, args.name)
    else:
        # Default: run all sites
        logger.info(f"No arguments — running {len(DEFAULT_SITES)} default sites.")
        for site in DEFAULT_SITES:
            try:
                result = run_pipeline(site["url"], site["name"])
                if result:
                    print(f"\n  {site['name']}: Grade={result['grade']}, Score={result['final_risk_score']}")
                    print(f"  Justification: {result.get('justification', 'N/A')[:120]}")
            except Exception as e:
                logger.error(f"Failed on {site['name']}: {e}")
        return

    if result:
        print(f"\nGrade: {result['grade']}")
        print(f"Score: {result['final_risk_score']}")
        print(f"Justification: {result.get('justification', 'N/A')}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
