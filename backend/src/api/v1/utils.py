from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from core.ioc import Inject
from services.auth import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin", auto_error=False)
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized",
    headers={"WWW-Authenticate": "Bearer"},
)
AUTH_TOKEN_KEY = "sns_auth_token"


async def get_user_id_or_raise(
    bearer_token: Annotated[str | None, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Inject(AuthService)],
    req: Request,
):
    cookie_token = req.cookies.get(AUTH_TOKEN_KEY)
    token = bearer_token or cookie_token
    if not token:
        raise credentials_exception from None
    payload = await auth_service.verfiy_token(token)
    return payload[auth_service.token_uid_key]


async def get_user_id_or_none(
    bearer_token: Annotated[str | None, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Inject(AuthService)],
    req: Request,
):
    try:
        return await get_user_id_or_raise(bearer_token, auth_service, req)
    except HTTPException:
        return None
