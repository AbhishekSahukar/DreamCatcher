from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
from app.interpreter import interpret_dream
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()


app.mount("/assets", StaticFiles(directory="app/static/assets"), name="assets")



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

@app.post("/analyse", response_model=InterpretationOutput)
async def analyze_dream(data: DreamInput):
    try:
        interpretation = interpret_dream(data.dream)
        return {"interpretation": interpretation}
    except Exception as e:
        import traceback
        print("🔥 Error during interpretation:", str(e))
        traceback.print_exc()
        raise e


@app.get("/")
def serve_frontend():
    return FileResponse("app/templates/index.html")
