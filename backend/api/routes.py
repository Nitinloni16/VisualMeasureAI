from fastapi import APIRouter, HTTPException
from backend.models.schemas import AnalysisRequest, ProductAnalysisResponse
from backend.services.vision_engine import get_vision_service

router = APIRouter()

@router.post("/analyze-product", response_model=ProductAnalysisResponse)
async def analyze_product(request: AnalysisRequest):
    """
    Analyzes product images to extract visual measurements.
    """
    if not request.image_urls:
        raise HTTPException(status_code=400, detail="At least one image URL must be provided.")
    
    if not request.image_urls:
        raise HTTPException(status_code=400, detail="At least one image URL must be provided.")
    
    print(f"Analyzing {len(request.image_urls)} URLs: {request.image_urls}")

    try:
        service = get_vision_service()
        # Convert Pydantic HttpUrl to string for the service
        url_strings = [str(url) for url in request.image_urls]
        result = await service.analyze_images(url_strings)
        
        # Pass back the product_id if provided
        if request.product_id:
            result.product_id = request.product_id
            
        print("Analysis successful")
        return result
    except Exception as e:
        print(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

from fastapi import UploadFile, File, Form
from typing import List
import base64

@router.post("/analyze/upload", response_model=ProductAnalysisResponse)
async def analyze_product_upload(
    files: List[UploadFile] = File(...),
    product_id: str = Form(None)
):
    """
    Analyzes uploaded product images.
    """
    if not files:
        raise HTTPException(status_code=400, detail="At least one image file must be uploaded.")

    image_urls = []
    
    try:
        for file in files:
            contents = await file.read()
            # Basic mime type inference or use file.content_type
            mime_type = file.content_type or "image/jpeg" 
            encoded_image = base64.b64encode(contents).decode("utf-8")
            data_url = f"data:{mime_type};base64,{encoded_image}"
            image_urls.append(data_url)
        
        print(f"Analyzing {len(image_urls)} uploaded images")
        service = get_vision_service()
        result = await service.analyze_images(image_urls)
        
        if product_id:
            result.product_id = product_id
            
        return result

    except Exception as e:
        print(f"Upload analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Upload analysis failed: {str(e)}")
