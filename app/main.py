from pathlib import Path
import traceback

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from app.interpreter import interpret_dream

app = FastAPI(title="DreamCatcher API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DreamInput(BaseModel):
    dream: str


class InterpretationOutput(BaseModel):
    interpretation: str


@app.get("/api/health")
def health_check():
    return {"status": "DreamCatcher API is running"}


@app.post("/analyse", response_model=InterpretationOutput)
async def analyse_dream(data: DreamInput):

    if not data.dream.strip():
        raise HTTPException(
            status_code=400,
            detail="Dream description cannot be empty."
        )

    try:
        interpretation = interpret_dream(data.dream)
        return {"interpretation": interpretation}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "dist"

if FRONTEND_DIR.exists():

    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIR / "assets"),
        name="assets",
    )

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_react_app(full_path: str):

        requested_path = FRONTEND_DIR / full_path

        # Serve actual files if they exist
        if requested_path.exists() and requested_path.is_file():
            return FileResponse(requested_path)

        # Otherwise return React app
        return FileResponse(FRONTEND_DIR / "index.html")