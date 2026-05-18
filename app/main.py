from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
import traceback

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


@app.get("/")
def health_check():
    return {"status": "DreamCatcher API is running"}


@app.post("/analyse", response_model=InterpretationOutput)
async def analyse_dream(data: DreamInput):
    if not data.dream.strip():
        raise HTTPException(status_code=400, detail="Dream description cannot be empty.")
    try:
        interpretation = interpret_dream(data.dream)
        return {"interpretation": interpretation}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))