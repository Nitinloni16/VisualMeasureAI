from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import List, Optional
from services.gateway.schemas import AnalysisRequest, ProductAnalysisResponse
from services.gateway.config import settings
import base64

app = FastAPI(title="Gateway Service", version="1.0.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VISION_SERVICE_URL = "http://localhost:8001/process"

@app.post("/api/v1/analyze-product", response_model=ProductAnalysisResponse)
async def analyze_product(request: AnalysisRequest):
    async with httpx.AsyncClient() as client:
        try:
            # Forwarding to Vision Service.
            # Convert Pydantic model to dict/json
            resp = await client.post(VISION_SERVICE_URL, json=request.model_dump(mode='json'), timeout=60.0)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Vision Service Error: {str(e)}")

@app.post("/api/v1/analyze/upload", response_model=ProductAnalysisResponse)
async def analyze_product_upload(
    files: List[UploadFile] = File(...),
    product_id: Optional[str] = Form(None)
):
    image_urls = []
    try:
        # Pre-process files into Base64 URLs here in Gateway (or could stream to Vision)
        # Doing it here keeps Vision simple (receiving list of strings)
        for file in files:
            contents = await file.read()
            mime_type = file.content_type or "image/jpeg"
            encoded_image = base64.b64encode(contents).decode("utf-8")
            data_url = f"data:{mime_type};base64,{encoded_image}"
            image_urls.append(data_url)
        
        # Construct payload for Vision Service
        payload = {
            "image_urls": image_urls,
            "product_id": product_id
        }

        async with httpx.AsyncClient() as client:
             resp = await client.post(VISION_SERVICE_URL, json=payload, timeout=60.0)
             resp.raise_for_status()
             return resp.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gateway Upload Error: {str(e)}")

@app.get("/")
def root():
    return {"message": "Gateway Service Online"}
