import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

from pipeline import run_research_pipeline

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI(title="ResearchMind - Multi-Agent AI System")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers to browser
    max_age=3600,
)


class QueryRequest(BaseModel):
    query: str
    use_gemini: bool = False


@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
def read_index() -> str:
    """Serve frontend HTML"""
    html_file = FRONTEND_DIR / "index.html"
    if not html_file.exists():
        return "<h1>Error: index.html not found at " + str(html_file) + "</h1>"
    with open(html_file, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/styles.css")
def read_styles() -> FileResponse:
    """Serve CSS stylesheet"""
    css_file = FRONTEND_DIR / "styles.css"
    if not css_file.exists():
        raise HTTPException(status_code=404, detail="CSS not found")
    return FileResponse(css_file, media_type="text/css; charset=utf-8")


@app.get("/app.js")
def read_app() -> FileResponse:
    """Serve JavaScript logic"""
    js_file = FRONTEND_DIR / "app.js"
    if not js_file.exists():
        raise HTTPException(status_code=404, detail="JavaScript not found")
    return FileResponse(js_file, media_type="application/javascript; charset=utf-8")


@app.get("/health")
def read_health() -> dict:
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/api/run")
def run_query(payload: QueryRequest) -> JSONResponse:
    """Execute multi-agent research pipeline"""
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        result = run_research_pipeline(query, use_gemini=payload.use_gemini)
        
        # Ensure result is properly formatted
        if not isinstance(result, dict):
            result = {"error": "Invalid response format"}
        
        # Ensure all required fields are present
        required_fields = ['query', 'steps', 'report', 'sources', 'feedback', 'usage']
        for field in required_fields:
            if field not in result:
                result[field] = None if field != 'sources' else []
        
        # Return with explicit JSON response
        return JSONResponse(
            content=result,
            status_code=200,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        # Return error in proper JSON format
        return JSONResponse(
            content={
                "error": str(exc),
                "query": query,
                "steps": [],
                "report": "",
                "sources": [],
                "feedback": f"Error: {str(exc)}"
            },
            status_code=500,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )


if __name__ == "__main__":
    import uvicorn
    
    # Detect if running on Hugging Face Spaces
    is_hf_space = os.getenv("SPACE_ID") is not None
    
    if is_hf_space:
        # Hugging Face Spaces uses port 7860
        port = 7860
        print("🚀 Running on Hugging Face Spaces (port 7860)")
    else:
        # Local development
        port = int(os.getenv("PORT", 8000))
        print(f"🚀 Running locally (port {port})")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
