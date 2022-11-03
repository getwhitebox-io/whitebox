from typing import List
from fastapi import APIRouter, Depends, status
from src.crud.performance_metrics import binary_classification_metrics, multi_classification_metrics
from src.crud.models import models
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.performanceMetric import BinaryClassificationMetrics, MultiClassificationMetrics
from src.utils.errors import errors


performance_metrics_router = APIRouter()


@performance_metrics_router.get(
    "/models/{model_id}/performance_metrics",
    tags=["Performance Metrics"],
    response_model=List[BinaryClassificationMetrics] | List[MultiClassificationMetrics],
    summary="Get all model's performance metrics",
    status_code=status.HTTP_200_OK,
)
async def get_all_models_performance_metrics(model_id: str, db: Session = Depends(get_db)):
    model = models.get(db, model_id)
    if model:
        if model.__dict__["type"] == "binary":
            return binary_classification_metrics.get_model_performance_metrics(db=db, model_id=model_id)
        else:
            return multi_classification_metrics.get_model_performance_metrics(db=db, model_id=model_id)
    else:
        return errors.not_found("Model not found")