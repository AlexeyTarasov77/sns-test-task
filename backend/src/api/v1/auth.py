from typing import Annotated
from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.ioc import Inject
from services.auth import AuthService
from dto import SignInDTO, SignUpDTO, UserDTO

router = APIRouter(prefix="/auth")

AuthServiceDep = Annotated[AuthService, Inject(AuthService)]

AUTH_TOKEN_KEY = "auth_token"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin", auto_error=False)
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_user_id_or_raise(
    token: Annotated[str | None, Depends(oauth2_scheme)],
    auth_service: AuthServiceDep,
):
    if not token:
        raise credentials_exception from None
    payload = await auth_service.verfiy_token(token)
    return payload[auth_service.token_uid_key]


@router.post("/signin")
async def signin(dto: SignInDTO, service: AuthServiceDep, resp: Response) -> UserDTO:
    res = await service.signin(dto)
    resp.set_cookie(AUTH_TOKEN_KEY, res.token)
    return res.user


@router.post("/signup")
async def signup(dto: SignUpDTO, service: AuthServiceDep):
    return await service.signup(dto)
