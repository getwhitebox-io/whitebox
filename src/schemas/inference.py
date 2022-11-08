from datetime import datetime
from typing import Any, Dict, Union, Optional
from pydantic import BaseModel
from src.schemas.base import ItemBase


class InferenceRowBase(BaseModel):
    model_id: str
    timestamp: Union[str, datetime]
    # Prediction is included into nonprocessed & processed
    nonprocessed: Dict[str, Any]
    processed: Dict[str, float]

    actual: Optional[Dict[str, Any]]


class Inference(InferenceRowBase, ItemBase):
    pass


class InferenceCreate(InferenceRowBase):
    pass
