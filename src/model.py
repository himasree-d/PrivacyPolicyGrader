import os
import json
import logging
from google import genai
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PolicyAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        
        self.client = genai.Client(api_key=self.api_key)
        # Updated based on debug_api.py results
        self.models_to_try = [
            'gemini-2.0-flash', 
            'gemini-2.5-flash', 
            'gemini-2.0-flash-lite', 
            'gemini-flash-latest', 
            'gemini-pro-latest'
        ]

    def analyze_chunks(self, chunks: List[str]) -> Dict:
        """Analyzes privacy policy chunks and returns structured JSON."""
        
        full_text = " ".join(chunks)[:15000]
        
        prompt = f"""
        Analyze the following privacy policy text and extract key information.
        Return the output STRICTLY in JSON format.
        
        JSON Structure:
        {{
            "data_collected": ["list of specific data points"],
            "third_party_sharing": ["who data is shared with"],
            "security_practices": ["security measures mentioned"],
            "user_rights": ["rights like access, deletion, etc."],
            "red_flags": ["vague terms, data selling, no user control"],
            "risk_score": 0-100,
            "justification": "short explanation for the score"
        }}
        
        Instructions:
        - Be conservative and precise.
        - Extract explicitly mentioned details.
        - Infer risks where terms are vague (e.g., 'may share', 'third party partners').
        - Risk Score: 0 is perfect privacy, 100 is extremely invasive.
        
        Privacy Policy Text:
        {full_text}
        """
        
        last_error = ""
        for model_name in self.models_to_try:
            try:
                logging.info(f"Attempting analysis with model: {model_name}")
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                
                content = response.text.strip()
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                    
                result = json.loads(content)
                logging.info(f"Successfully analyzed policy using {model_name}.")
                return result
                
            except Exception as e:
                last_error = str(e)
                logging.warning(f"Model {model_name} failed: {last_error}")
                continue
        
        logging.error(f"All models failed. Last error: {last_error}")
        return {
            "error": last_error,
            "data_collected": [],
            "third_party_sharing": [],
            "security_practices": [],
            "user_rights": [],
            "red_flags": ["Failed to process policy"],
            "risk_score": 100,
            "justification": f"Analysis failed. Please check your API key and model access. Error: {last_error}"
        }

if __name__ == "__main__":
    pass
