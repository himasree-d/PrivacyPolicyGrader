import requests
from bs4 import BeautifulSoup
import logging
import os
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PolicyScraper:
    def __init__(self, timeout=20):
        self.timeout = timeout
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
        }

    def scrape(self, url):
        """Scrapes text content from a given URL."""
        try:
            logging.info(f"Scraping URL: {url}")
            
            # Instagram specific referer
            if "instagram" in url:
                self.headers['Referer'] = 'https://www.google.com/'
            
            time.sleep(2) # Be gentle
            
            response = self.session.get(url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            
            if response.status_code != 200:
                logging.warning(f"Received status code {response.status_code} for {url}. Attempting a fallback approach...")
                response = requests.get(url, timeout=self.timeout) # Simple request as fallback
            
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unnecessary elements
            for tag in soup(["script", "style", "nav", "footer", "header", "aside", "svg", "form"]):
                tag.decompose()

            # Get text
            text = soup.get_text(separator=' ')
            
            # Clean up whitespace
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            text = '\n'.join(lines)
            
            logging.info(f"Successfully scraped {len(text)} characters from {url}")
            return text
            
        except Exception as e:
            logging.error(f"Error scraping {url}: {str(e)}")
            return None

if __name__ == "__main__":
    pass
