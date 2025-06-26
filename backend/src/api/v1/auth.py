from typing import Annotated
from fastapi import APIRouter, Response
from core.ioc import Inject
from services.auth import AuthService
from dto import SignInDTO, SignUpDTO, UserDTO

router = APIRouter(prefix="/auth")

AuthServiceDep = Annotated[AuthService, Inject(AuthService)]

AUTH_TOKEN_KEY = "auth_token"


@router.post("/signin")
async def signin(dto: SignInDTO, service: AuthServiceDep, resp: Response) -> UserDTO:
    res = await service.signin(dto)
    resp.set_cookie(AUTH_TOKEN_KEY, res.token)
    return res.user


@router.post("/signup")
async def signup(dto: SignUpDTO, service: AuthServiceDep):
    return await service.signup(dto)
