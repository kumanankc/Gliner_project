from gliner import GLiNER
import logging
from typing import List, Dict, Any
from .config import settings

logger = logging.getLogger(__name__)

class NERModel:
    def __init__(self, model_name: str = settings.MODEL_NAME):
        try:
            logger.info(f"Loading model {model_name}...")
            self.model = GLiNER.from_pretrained(model_name)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise RuntimeError(f"Failed to load model: {str(e)}")

    def predict(self, text: str, labels: List[str]) -> List[Dict[str, Any]]:
        """Predict entities in the given text."""
        try:
            # Adding expected labels mapping
            label_mapping = {
                "PERSON": "person",
                "DATE": "date",
                "ORG": "teams",
                "AWARD": "award",
                "COMPETITION": "competitions"
            }
            
            predictions = self.model.predict_entities(text, labels)
            
            # Format predictions to match expected output
            entities = []
            for pred in predictions:
                if isinstance(pred, dict):
                    # Map the label to expected format
                    mapped_label = label_mapping.get(pred.get("label", ""), pred.get("label", ""))
                    entity = {
                        "text": str(pred.get("text", "")),
                        "label": mapped_label,
                        "start": int(pred.get("start", 0)),
                        "end": int(pred.get("end", 0)),
                        "score": float(pred.get("score", 1.0))
                    }
                    entities.append(entity)
                else:
                    logger.warning(f"Unexpected prediction format: {pred}")

            # Sort entities by their appearance in text (start position)
            entities = sorted(entities, key=lambda x: x["start"])
            logger.debug(f"Found {len(entities)} entities")
            return entities
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise RuntimeError(f"Prediction failed: {str(e)}")

    def warm_up(self) -> None:

        try:
            sample_text = """Cristiano Ronaldo dos Santos Aveiro is a Portuguese professional footballer 
            who plays for Al Nassr and the Portugal national team."""
            sample_labels = ["person", "team", "date", "award", "competitions"]
            result = self.predict(sample_text, sample_labels)
            logger.info(f"Model warm-up completed successfully. Found {len(result)} entities.")
        except Exception as e:
            logger.warning(f"Model warm-up failed: {str(e)}")