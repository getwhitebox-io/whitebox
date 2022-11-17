from requests import Session
from fastapi import Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from src.core.db import get_db
from src.utils.tokens import create_access_token
from src.middleware.auth import get_current_user
from src.crud.users import users
from src.schemas.auth import Token
from src.schemas.user import User
from src.utils.errors import add_error_responses, errors

auth_router = APIRouter()


@auth_router.post(
    "/auth/token",
    tags=["Auth"],
    response_model=Token,
    summary="Get access token",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def get_access_token(
    db: Session = Depends(get_db), body: OAuth2PasswordRequestForm = Depends()
):
    user_in_db = users.authenticate(db, email=body.username, password=body.password)
    if not user_in_db:
        return errors.not_found("No user found")

    return {
        "access_token": create_access_token(user_in_db),
        "token_type": "bearer",
    }


@auth_router.post(
    "/auth/me",
    tags=["Auth"],
    response_model=User,
    summary="Get active user",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401]),
)
async def get_active_user(active_user: User = Depends(get_current_user)):
    if not active_user:
        return errors.unauthorized("Not logged in")
    active_user["password"] = None
    return active_user
