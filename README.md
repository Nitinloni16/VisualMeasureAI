# Visual Product Measurement System

An AI-powered system to measure product dimensions from images using a reference object.
Now architected as scalable Microservices.

## Features
- **Visual-Only Analysis**: Strict prompt engineering ensures no merchandising fluff.
- **-5.0 to +5.0 Scoring**: Quantitative scoring for dimensions like Gender Expression, Visual Weight, etc.
- **Strict JSON Output**: Deterministic schema validation.
- **Microservices**: Separation of concerns between API Gateway and Vision Processing.
- **Tech Stack**: Python (FastAPI), React (Vite), Pydantic, Pytest.

## System Design Restructuring: Microservices Architecture

To improve scalability and separation of concerns, the system is split into separate services.

### Proposed Architecture

#### 1. Gateway Service (`services/gateway`)
- **Role**: Entry point for the frontend / public API.
- **Port**: 8000 (Same as before, so Frontend doesn't break).
- **Responsibilities**:
  - Authentication (Future proofing)
  - Request Validation
  - Routing to backend services
  - Aggregating results

#### 2. Vision Service (`services/vision`)
- **Role**: Dedicated AI/Vision processing unit.
- **Port**: 8001.
- **Responsibilities**:
  - Handling LLM interactions (Groq/OpenAI).
  - Image processing.
  - Stateless execution.

### Directory Structure
```text
/
├── frontend/               (Unchanged)
├── services/
│   ├── gateway/            (Main API entry point)
│   │   ├── main.py
│   │   ├── config.py
│   │   └── routers/
│   └── vision/             (AI Logic)
│       ├── main.py
│       ├── core/
│       └── engine/
└── requirements.txt
└── DataStore/ 
├── api/
│   └── routes.py
├── core/
│   └── config.py
├── models/
│   └── schemas.py
├── services/
│   ├── prompt_manager.py
│   └── vision_engine.py
└── tests/
    └── test_api.py
```

### System Architecture & Fallback Logic

```mermaid
graph TD
    User[User / Frontend] -->|HTTP Request| Gateway[Gateway Service :8000]
    Gateway -->|Forward Request| Vision[Vision Service :8001]
    
    subgraph Vision Logic
        Vision -->|Start Analysis| CheckConfig{Provider Config}
        CheckConfig -->|LLM_PROVIDER="groq"| TryGroq[Attempt Groq API]
        CheckConfig -->|LLM_PROVIDER="mock"| SmartMock[Smart Mock Generator]
        
        TryGroq -->|Success| SuccessResult[Return Analysis]
        TryGroq --x|Error / No Key| Fallback[**Fallback Triggered**]
        
        Fallback -->|Switch to Backup| SmartMock
        SmartMock -->|Generate Dynamic Result based on Hash| SuccessResult
    end
    
    SuccessResult --> Vision
    Vision --> Gateway
    Gateway --> User
```

## Setup & Running

### Prerequisites
- Python 3.11.6
- Node.js 22.13.1

### 1. Backend Setup

You need to run **two** terminal processes for the backend services.

**Terminal 1: Gateway Service**
```bash
# In root directory services/gateway
venv/Scripts/python -m uvicorn services.gateway.main:app --port 8000 --reload
```

**Terminal 2: Vision Service**
```bash
# In root directory services/vision
venv/Scripts/python -m uvicorn services.vision.main:app --port 8001 --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: `http://localhost:5173`

## Usage
1. Open the frontend URL.
2. Enter a product image URL or Upload an image.
3. Click "Analyze".
4. The Gateway forwards the request to the Vision Service and returns the results.
