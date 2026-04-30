class PolicyGrader:
    def __init__(self):
        pass

    def get_grade(self, risk_score: int) -> str:
        """
        Score 0–20 → A
        Score 21–40 → B
        Score 41–60 → C
        Score 61–80 → D
        Score 81–100 → F
        """
        if risk_score <= 20:
            return "A"
        elif risk_score <= 40:
            return "B"
        elif risk_score <= 60:
            return "C"
        elif risk_score <= 80:
            return "D"
        else:
            return "F"

    def calculate_risk_adjustments(self, extracted_data: dict) -> int:
        """
        Optionally adjust the score based on specific presence of red flags 
        if the LLM missed the intensity.
        """
        base_score = extracted_data.get('risk_score', 50)
        red_flags = extracted_data.get('red_flags', [])
        
        # Penalize for common critical red flags
        critical_flags = ["data selling", "third party sale", "vague", "no encryption", "no control"]
        
        for flag in red_flags:
            for critical in critical_flags:
                if critical in flag.lower():
                    base_score += 5
        
        return min(100, max(0, base_score))

    def process(self, extracted_data: dict) -> dict:
        """Adds grade and final score to the extracted data."""
        final_score = self.calculate_risk_adjustments(extracted_data)
        grade = self.get_grade(final_score)
        
        extracted_data['final_risk_score'] = final_score
        extracted_data['grade'] = grade
        
        return extracted_data

if __name__ == "__main__":
    grader = PolicyGrader()
    test_data = {"risk_score": 35, "red_flags": ["vague terms"]}
    result = grader.process(test_data)
    print(f"Final Grade: {result['grade']} (Score: {result['final_risk_score']})")
