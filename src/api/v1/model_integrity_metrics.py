from typing import List
from fastapi import APIRouter, Depends, status
from src import crud
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.middleware.auth import authenticate_user
from src.schemas.modelIntegrityMetric import ModelIntegrityMetric
from src.utils.errors import add_error_responses, errors


model_integrity_metrics_router = APIRouter()


@model_integrity_metrics_router.get(
    "/models/{model_id}/model-integrity-metrics",
    tags=["Model Integrity Metrics"],
    response_model=List[ModelIntegrityMetric],
    summary="Get all model's model integrity metrics",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_all_models_model_integrity_metrics(
    model_id: str,
    db: Session = Depends(get_db),
    authenticated: bool = Depends(authenticate_user),
):

    model = crud.models.get(db, model_id)
    if model:
        return crud.model_integrity_metrics.get_model_model_integrity_metrics(
            db=db, model_id=model_id
        )
    else:
        return errors.not_found("Model not found")
