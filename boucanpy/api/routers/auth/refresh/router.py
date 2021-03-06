from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from boucanpy.core.auth import PasswordAuthResponse
from boucanpy.db.models.user import User

from boucanpy.core.security import (
    create_bearer_token,
    current_user,
    TokenPayload,
    ScopedTo,
)

router = APIRouter()
options = {"prefix": "/auth"}


@router.post("/refresh", name="auth.refresh", response_model=PasswordAuthResponse)
async def login(
    token: TokenPayload = Depends(ScopedTo("refresh")),
    user: User = Depends(current_user),
):
    token = create_bearer_token(
        data={"sub": token.sub, "scopes": " ".join(token.scopes)}
    )
    return PasswordAuthResponse(token_type="bearer", access_token=str(token))
