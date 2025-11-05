from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
from app.interpreter import interpret_dream
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from fastapi.responses import FileResponse
import os

app = FastAPI()

# ✅ Add CORS middleware for local dev
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

@app.post("/download-pdf")
async def download_pdf(request: DreamInput):
    dream_text = request.dream
    interpretation = interpret_dream(dream_text)

    file_path = "dream_interpretation.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    flowables = []

    flowables.append(Paragraph("<b>Dream Interpretation</b>", styles["Title"]))
    flowables.append(Spacer(1, 12))
    flowables.append(Paragraph(f"<b>Dream:</b> {dream_text}", styles["BodyText"]))
    flowables.append(Spacer(1, 8))
    flowables.append(Paragraph(f"<b>Interpretation:</b> {interpretation}", styles["BodyText"]))

    doc.build(flowables)
    return FileResponse(path=file_path, filename="dream_interpretation.pdf", media_type="application/pdf")

