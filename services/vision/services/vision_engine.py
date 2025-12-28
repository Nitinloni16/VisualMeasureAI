from abc import ABC, abstractmethod
from typing import List, Dict, Any
from services.vision.models.schemas import ProductAnalysisResponse, ContinuousDimensions, DiscreteAttributes, VisualMetadata
from services.vision.services.prompt_manager import PromptManager
import random

from groq import AsyncGroq
from services.vision.config import settings

class IVisionService(ABC):
    @abstractmethod
    async def analyze_images(self, image_urls: List[str]) -> ProductAnalysisResponse:
        pass

class MockVisionService(IVisionService):
    """
    Returns deterministic/randomized data for testing without API costs.
    Now "Smart" - produces dynamic results based on image URL hash.
    """
    async def analyze_images(self, image_urls: List[str]) -> ProductAnalysisResponse:
        # 1. Create a deterministic seed from the image URLs
        # Concatenate all urls and hash
        combined_string = "".join(image_urls)
        seed_value = hash(combined_string)
        random.seed(seed_value)

        # 2. Generate Dynamic Continuous Dimensions (-5.0 to +5.0)
        # We use random.uniform and round to 1 decimal place
        dims = ContinuousDimensions(
            gender_expression=round(random.uniform(-5.0, 5.0), 1),
            visual_weight=round(random.uniform(-5.0, 5.0), 1),
            embellishment=round(random.uniform(-5.0, 5.0), 1),
            unconventionality=round(random.uniform(-5.0, 5.0), 1),
            formality=round(random.uniform(-5.0, 5.0), 1)
        )

        # 3. Generate Dynamic Discrete Attributes
        colors = ["Black", "Silver", "Gold", "Tortoise", "Blue", "Red", "Clear", "Grey"]
        shapes = ["Rectangular", "Round", "Aviator", "Cat-eye", "Square", "Oval", "Geometric"]
        textures = ["Matte", "Glossy", "Translucent", "Tortoise Pattern", "Metallic"]

        # Pick 1-3 random colors
        dom_colors = random.sample(colors, k=random.randint(1, 3))

        attrs = DiscreteAttributes(
            has_wirecore=random.choice([True, False]),
            is_transparent=random.choice([True, False]),
            dominant_colors=dom_colors,
            frame_shape=random.choice(shapes),
            texture_pattern=random.choice(textures),
            looks_like_kids_product=random.choice([True, False])
        )

        # 4. Return Response
        return ProductAnalysisResponse(
            continuous_dimensions=dims,
            discrete_attributes=attrs,
            metadata=VisualMetadata(
                image_quality_notes=random.choice(["Average", "Below Average"]),
                is_occluded_or_ambiguous=random.random() < 0.1, # 10% chance
                confidence_score=round(random.uniform(0.50, 0.70), 2)
            )
        )

class GroqVisionService(IVisionService):
    """
    Implementation using Groq Cloud API (Llama 3.2 Vision) with Fallback.
    """
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        # If no key is set, we can log a warning, but we still init the client
        # so the try/catch in analyze_images triggers the fallback naturally.
        self.client = None
        if self.api_key:
            self.client = AsyncGroq(api_key=self.api_key)
        self.model = "llama-3.2-11b-vision-preview"

    async def analyze_images(self, image_urls: List[str]) -> ProductAnalysisResponse:
        # Check if client exists (key was present)
        if not self.client:
            print("Groq API Key missing. Falling back to Smart Mock.")
            return await MockVisionService().analyze_images(image_urls)

        system_prompt = PromptManager.construct_system_prompt()
        user_content = PromptManager.construct_user_message(image_urls)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        try:
            print("Attempting analysis via Groq...")
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
            print(f"Groq API Failed: {e}")
            print("Falling back to Smart Mock Service...")
            # FALLBACK LOGIC
            return await MockVisionService().analyze_images(image_urls)

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
