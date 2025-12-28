from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.vision.services.vision_engine import get_vision_service
from services.vision.config import settings

app = FastAPI(title="Vision Service", version="1.0.0")

class AnalysisRequest(BaseModel):
    image_urls: List[str]
    product_id: Optional[str] = None

@app.post("/process")
async def process_images(request: AnalysisRequest):
    try:
        service = get_vision_service()
        result = await service.analyze_images(request.image_urls)
        if request.product_id:
            result.product_id = request.product_id
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "vision"}
