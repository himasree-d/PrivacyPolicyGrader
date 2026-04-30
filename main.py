import os
import json
import logging
from src.scraper import PolicyScraper
from src.preprocess import TextPreprocessor
from src.model import PolicyAnalyzer
from src.grader import PolicyGrader
from dotenv import load_dotenv

# Load environment variables (for GOOGLE_API_KEY)
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline(url_or_text, name="sample"):
    """Runs the full privacy policy grading pipeline."""
    logging.info(f"Starting pipeline for: {name}")
    
    # 1. Ingestion
    scraper = PolicyScraper()
    if url_or_text.startswith("http"):
        raw_text = scraper.scrape(url_or_text)
    else:
        raw_text = url_or_text
        
    if not raw_text:
        logging.error("Failed to get raw text.")
        return None

    # 2. Preprocessing
    preprocessor = TextPreprocessor()
    cleaned_text = preprocessor.clean_text(raw_text)
    chunks = preprocessor.chunk_text(cleaned_text)
    
    # NEW: Save cleaned text to data folder to meet "Data Loaded" requirement
    preprocessor.save_processed({"name": name, "chunks": chunks}, f"{name.lower().replace(' ', '_')}_data.json")
    
    # 3. Model Analysis
    analyzer = PolicyAnalyzer()
    extracted_data = analyzer.analyze_chunks(chunks)
    
    # 4. Grading
    grader = PolicyGrader()
    final_results = grader.process(extracted_data)
    
    # 5. Output
    output_filename = f"{name.lower().replace(' ', '_')}_results.json"
    output_path = os.path.join('results', output_filename)
    os.makedirs('results', exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(final_results, f, indent=4)
        
    logging.info(f"Pipeline complete. Results saved to {output_path}")
    return final_results

if __name__ == "__main__":
    # Example usage
    test_sites = [
        {"name": "Google", "url": "https://policies.google.com/privacy"},
        {"name": "Instagram", "url": "https://help.instagram.com/519522125107875"},
        {"name": "Random Site", "url": "https://www.freecodecamp.org/news/privacy-policy/"}
    ]
    
    for site in test_sites:
        try:
            print(f"\n--- Processing {site['name']} ---")
            results = run_pipeline(site['url'], site['name'])
            if results:
                print(f"Grade: {results['grade']}")
                print(f"Score: {results['final_risk_score']}")
                print(f"Justification: {results['justification']}")
        except Exception as e:
            print(f"Failed to process {site['name']}: {e}")
