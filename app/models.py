from pydantic import BaseModel

class DreamRequest(BaseModel):
    dream: str