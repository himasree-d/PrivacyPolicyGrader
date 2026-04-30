from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
from main import run_pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Privacy Policy Grader API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None
    name: str = "custom"

@app.post("/analyze")
async def analyze_policy(request: AnalyzeRequest):
    input_data = request.url if request.url else request.text
    if not input_data:
        raise HTTPException(status_code=400, detail="Either URL or text must be provided.")
    
    try:
        results = run_pipeline(input_data, request.name)
        if results:
            return results
        else:
            raise HTTPException(status_code=500, detail="Pipeline failed to produce results.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
