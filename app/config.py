from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "GLiNER Entity Extraction API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    MODEL_NAME: str = "urchade/gliner_medium-v2"
    DEFAULT_LABELS: List[str] = ["person", "award", "date", "competitions", "teams"]
    
    MAX_TEXT_LENGTH: int = 10000
    MIN_CONFIDENCE_SCORE: float = 0.5

    class Config:
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()