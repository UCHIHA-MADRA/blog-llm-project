from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import json
import time
from typing import Optional
import os

app = FastAPI(title="Blog LLM API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"

class BlogRequest(BaseModel):
    topic: str
    type: str = "general"
    word_count: int = 500
    tone: str = "professional"
    audience: str = "general"

class BlogResponse(BaseModel):
    content: str
    word_count: int
    generation_time: float
    model_used: str

def create_blog_prompt(request: BlogRequest) -> str:
    """Create a structured prompt for blog generation"""
    
    prompt = f"""Write a {request.word_count}-word blog post about "{request.topic}".

Blog Type: {request.type}
Writing Tone: {request.tone}
Target Audience: {request.audience}
Word Count Target: {request.word_count} words

Requirements:
- Write in a {request.tone} tone suitable for {request.audience}
- Include an engaging title
- Structure with clear sections and headings
- Provide valuable insights and actionable information
- Make it approximately {request.word_count} words
- Use markdown formatting for headings

Please write the complete blog post now:"""

    return prompt

def generate_with_ollama(prompt: str) -> str:
    """Generate content using Ollama API"""
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 2000
        }
    }
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            raise HTTPException(
                status_code=500, 
                detail=f"Ollama API error: {response.status_code}"
            )
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503, 
            detail=f"Cannot connect to Ollama: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Blog LLM API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Ollama connection
        test_response = requests.get("http://localhost:11434/api/tags", timeout=5)
        ollama_status = "healthy" if test_response.status_code == 200 else "unhealthy"
    except:
        ollama_status = "unavailable"
    
    return {
        "status": "healthy",
        "ollama_status": ollama_status,
        "model": MODEL_NAME,
        "timestamp": time.time()
    }

@app.post("/generate-blog", response_model=BlogResponse)
async def generate_blog(request: BlogRequest):
    """Generate a blog post based on the request"""
    
    start_time = time.time()
    
    # Validate input
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    
    if request.word_count < 100 or request.word_count > 2000:
        raise HTTPException(status_code=400, detail="Word count must be between 100 and 2000")
    
    # Create prompt
    prompt = create_blog_prompt(request)
    
    # Generate content
    content = generate_with_ollama(prompt)
    
    # Calculate metrics
    generation_time = time.time() - start_time
    word_count = len(content.split())
    
    return BlogResponse(
        content=content,
        word_count=word_count,
        generation_time=generation_time,
        model_used=MODEL_NAME
    )

@app.get("/models")
async def list_models():
    """List available models in Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Cannot connect to Ollama"}
    except:
        return {"error": "Ollama not available"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)