from pydantic import BaseModel, Field
from typing import List

class TextInput(BaseModel):
    text: str
    labels: List[str]
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "Cristiano Ronaldo plays for Al Nassr.",
                "labels": ["person", "team"]
            }
        }
    }

class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int
    score: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "Cristiano Ronaldo",
                "label": "person",
                "start": 0,
                "end": 17,
                "score": 0.99
            }
        }
    }

class EntityResponse(BaseModel):
    entities: List[Entity]

class HealthResponse(BaseModel):
    status: str
    model_name: str
    version: str = "1.0.0"