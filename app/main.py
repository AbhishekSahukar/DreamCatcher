from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from app.models import DreamRequest
from app.interpreter import interpret_dream

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static + templates
app.mount(
    "/assets",
    StaticFiles(directory="app/static/assets"),
    name="assets"
)

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
@app.head("/")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/analyse")
async def analyse_dream(data: DreamRequest):

    interpretation = interpret_dream(data.dream)

    return JSONResponse(
        content={
            "interpretation": interpretation
        }
    )