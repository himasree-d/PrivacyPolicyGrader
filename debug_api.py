import requests
import json

def test_analyze():
    url = "http://localhost:8000/analyze"
    payload = {
        "url": "https://www.freecodecamp.org/news/privacy-policy/",
        "name": "API Debug Test"
    }
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Success!")
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    test_analyze()
