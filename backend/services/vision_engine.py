from abc import ABC, abstractmethod
from typing import List, Dict, Any
from backend.models.schemas import ProductAnalysisResponse, ContinuousDimensions, DiscreteAttributes, VisualMetadata
from backend.services.prompt_manager import PromptManager
import random

from groq import AsyncGroq
from backend.core.config import settings

class IVisionService(ABC):
    @abstractmethod
    async def analyze_images(self, image_urls: List[str]) -> ProductAnalysisResponse:
        pass

class MockVisionService(IVisionService):
    """
    Returns deterministic/randomized data for testing without API costs.
    """
    async def analyze_images(self, image_urls: List[str]) -> ProductAnalysisResponse:
        # Simulate processing - In a real mock, we might hash the URL to get stable randoms
        # For this prototype, we'll return a fixed reasonable sample to show plumbing works.
        
        return ProductAnalysisResponse(
            continuous_dimensions=ContinuousDimensions(
                gender_expression=0.5, # Slightly feminine/neutral
                visual_weight=-2.0,    # Light
                embellishment=-4.5,    # Very simple
                unconventionality=-3.0,# Classic
                formality=1.0          # Smart Casual
            ),
            discrete_attributes=DiscreteAttributes(
                has_wirecore=True,
                is_transparent=False,
                dominant_colors=["Black", "Silver"],
                frame_shape="Rectangular",
                texture_pattern="Matte",
                looks_like_kids_product=False
            ),
            metadata=VisualMetadata(
                image_quality_notes="Mock analysis - image not actually processed.",
                is_occluded_or_ambiguous=False,
                confidence_score=0.99
            )
        )

class GroqVisionService(IVisionService):
    """
    Implementation using Groq Cloud API (Llama 3.2 Vision).
    """
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set in configuration.")
        self.client = AsyncGroq(api_key=self.api_key)
        self.model = "llama-3.2-11b-vision-preview"

    async def analyze_images(self, image_urls: List[str]) -> ProductAnalysisResponse:
        system_prompt = PromptManager.construct_system_prompt()
        user_content = PromptManager.construct_user_message(image_urls)
        
        # Adapt user_content for Groq if needed, or assume standard OpenAI format works (it usually does for Groq)
        # Groq expects:
        # { "type": "image_url", "image_url": { "url": "..." } }
        # The prompt manager likely generates compatible format.
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,
                max_tokens=1024,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return ProductAnalysisResponse.model_validate_json(content)
        except Exception as e:
            # Fallback or re-raise
            print(f"Groq API Error: {e}")
            raise e

class OpenAIVisionService(IVisionService):
    """
    Real implementation using OpenAI API (requires API KEY).
    """
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        # client = AsyncOpenAI(api_key=api_key) 

    async def analyze_images(self, image_urls: List[str]) -> ProductAnalysisResponse:
        # This would call the real LLM.
        # Structure:
        # messages = [
        #     {"role": "system", "content": PromptManager.construct_system_prompt()},
        #     {"role": "user", "content": PromptManager.construct_user_message(image_urls)}
        # ]
        # response = await client.chat.completions.create(...)
        # return ProductAnalysisResponse.model_validate_json(response.choices[0].message.content)
        raise NotImplementedError("OpenAI Service requires a valid API key and dependency.")

def get_vision_service() -> IVisionService:
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "groq":
        return GroqVisionService()
    elif provider == "openai":
        return OpenAIVisionService()
    else:
        return MockVisionService()
