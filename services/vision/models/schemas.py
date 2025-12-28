from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from enum import Enum

class GenderExpression(float):
    """Score from -5.0 (Masculine) to +5.0 (Feminine)"""
    pass

class VisualWeight(float):
    """Score from -5.0 (Sleek/Light) to +5.0 (Bold/Heavy)"""
    pass

class Embellishment(float):
    """Score from -5.0 (Simple) to +5.0 (Ornate)"""
    pass

class Unconventionality(float):
    """Score from -5.0 (Classic) to +5.0 (Avant-Garde)"""
    pass

class Formality(float):
    """Score from -5.0 (Casual) to +5.0 (Formal)"""
    pass

class ContinuousDimensions(BaseModel):
    gender_expression: float = Field(..., ge=-5.0, le=5.0, description="Masculine (-5.0) to Feminine (5.0)")
    visual_weight: float = Field(..., ge=-5.0, le=5.0, description="Sleek/Light (-5.0) to Bold/Heavy (5.0)")
    embellishment: float = Field(..., ge=-5.0, le=5.0, description="Simple (-5.0) to Ornate (5.0)")
    unconventionality: float = Field(..., ge=-5.0, le=5.0, description="Classic (-5.0) to Avant-Garde (5.0)")
    formality: float = Field(..., ge=-5.0, le=5.0, description="Casual (-5.0) to Formal (5.0)")

class DiscreteAttributes(BaseModel):
    has_wirecore: bool = Field(..., description="Visible wirecore in temples")
    is_transparent: bool = Field(..., description="Frame material allows light through")
    dominant_colors: List[str] = Field(..., description="List of visually dominant colors")
    frame_shape: str = Field(..., description="e.g., Round, Square, Cat-eye, Aviator")
    texture_pattern: Optional[str] = Field(None, description="Visible surface texture or pattern (e.g., Tortoise, Matte)")
    looks_like_kids_product: bool = Field(..., description="Visually obvious sizing or styling for children")

class VisualMetadata(BaseModel):
    image_quality_notes: str = Field(..., description="Observations about image clarity, lighting, resolution")
    is_occluded_or_ambiguous: bool = Field(..., description="If essential parts are hidden or unclear")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Overall confidence in the visual analysis (0.0 to 1.0)")

class ProductAnalysisResponse(BaseModel):
    product_id: Optional[str] = None
    continuous_dimensions: ContinuousDimensions
    discrete_attributes: DiscreteAttributes
    metadata: VisualMetadata

class AnalysisRequest(BaseModel):
    image_urls: List[HttpUrl]
    product_id: Optional[str] = None
