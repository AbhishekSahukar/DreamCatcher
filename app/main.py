from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import traceback
from app.interpreter import interpret_dream
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

<<<<<<< HEAD
os.makedirs("app/static/assets", exist_ok=True)
os.makedirs("app/templates", exist_ok=True)
app = FastAPI()


app.mount("/assets", StaticFiles(directory="app/static/assets"), name="assets")




=======
load_dotenv()

app = FastAPI(title="DreamCatcher API")

>>>>>>> 142df6a (Readme and code fix)
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
async def analyze_dream(data: DreamInput):
    if not data.dream.strip():
        raise HTTPException(status_code=400, detail="Dream description cannot be empty.")
    try:
        interpretation = interpret_dream(data.dream)
        return {"interpretation": interpretation}
    except Exception as e:
<<<<<<< HEAD
        import traceback
        print("🔥 Error during interpretation:", str(e))
        traceback.print_exc()
        raise e


@app.get("/")
def serve_frontend():
    return FileResponse("app/templates/index.html")
=======
        raise HTTPException(status_code=500, detail=str(e))
>>>>>>> 142df6a (Readme and code fix)
