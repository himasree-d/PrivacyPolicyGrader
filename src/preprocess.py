import re
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TextPreprocessor:
    def __init__(self, chunk_size=3000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def clean_text(self, text):
        """Basic text cleaning."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that aren't useful
        text = re.sub(r'[^\x00-\x7f]', r'', text) 
        return text.strip()

    def chunk_text(self, text):
        """Splits text into manageable chunks for LLM."""
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += (self.chunk_size - self.chunk_overlap)
            
        logging.info(f"Split text into {len(chunks)} chunks.")
        return chunks

    def save_processed(self, data, filename):
        """Saves processed data to a JSON file."""
        output_path = os.path.join('data', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Saved processed data to {output_path}")

if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    sample_text = "This is a test privacy policy. It has many words. " * 100
    cleaned = preprocessor.clean_text(sample_text)
    chunks = preprocessor.chunk_text(cleaned)
    print(f"Chunks: {len(chunks)}")
