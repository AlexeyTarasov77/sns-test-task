from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.ioc import Inject
from services.auth import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin", auto_error=False)
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_user_id_or_raise(
    token: Annotated[str | None, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Inject(AuthService)],
):
    if not token:
        raise credentials_exception from None
    payload = await auth_service.verfiy_token(token)
    return payload[auth_service.token_uid_key]
