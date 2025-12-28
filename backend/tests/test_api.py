from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_analyze_product_success():
    payload = {
        "image_urls": ["http://example.com/image1.jpg"],
        "product_id": "test-123"
    }
    response = client.post("/api/v1/analyze-product", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == "test-123"
    assert "continuous_dimensions" in data
    assert "discrete_attributes" in data
    assert "metadata" in data
    
    # Verify range checks (Mock returns values within range, but good to check)
    dims = data["continuous_dimensions"]
    assert -5.0 <= dims["gender_expression"] <= 5.0

def test_analyze_product_no_images():
    payload = {
        "image_urls": []
    }
    response = client.post("/api/v1/analyze-product", json=payload)
    assert response.status_code == 422 # Pydantic validation error for empty list or 400 from our logic? 
    # Pydantic default for List is it can be empty unless constrained. 
    # Our logic in routes.py raises 400.
    # Let's check if pydantic allows empty list. Yes by default.
    # But wait, HttpUrl list... Pydantic might let it pass.
    # Our code: if not request.image_urls: raise 400.
    
    # If the list is empty, our code catches it.
    assert response.status_code == 400

def test_analyze_product_invalid_url():
    payload = {
        "image_urls": ["not-a-url"]
    }
    response = client.post("/api/v1/analyze-product", json=payload)
    assert response.status_code == 422 # Pydantic validation error
