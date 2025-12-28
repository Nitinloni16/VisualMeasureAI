from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered Visual Product Measurement System"
    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: list[str] = ["*"] # Allow all for prototype simplicity

    # LLM Configuration
    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    LLM_PROVIDER: str = "mock" # options: "mock", "groq", "openai"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
