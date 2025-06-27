from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from api.v1.utils import AUTH_TOKEN_KEY, get_user_id_or_none, get_user_id_or_raise
from core.ioc import Inject
from services.auth import AuthService
from dto import SignInDTO, SignUpDTO, UserDTO, UserExtendedDTO, UserTelegramAccDTO
from services.telegram import TelegramService

router = APIRouter(prefix="/auth")

AuthServiceDep = Annotated[AuthService, Inject(AuthService)]
TelegramServiceDep = Annotated[TelegramService, Inject(TelegramService)]

cookie_attrs = {
    "httponly": True,
    "secure": True,
    "samesite": "none",
}


@router.post("/signin")
async def signin(dto: SignInDTO, service: AuthServiceDep, resp: Response) -> UserDTO:
    res = await service.signin(dto)
    resp.set_cookie(
        AUTH_TOKEN_KEY,
        res.token,
        int(service.auth_token_ttl.total_seconds()),
        **cookie_attrs,
    )
    return res.user


@router.post("/signup")
async def signup(dto: SignUpDTO, service: AuthServiceDep):
    return await service.signup(dto)


@router.get("/me")
async def get_me(
    user_id: Annotated[int, Depends(get_user_id_or_raise)],
    auth_service: AuthServiceDep,
    tg_service: TelegramServiceDep,
) -> UserExtendedDTO:
    user = await auth_service.get_current_user(user_id)
    user_tg_acc_dto = None
    if user.tg_account:
        tg_acc_info = await tg_service.get_account_info(user.tg_account.id)
        user_tg_acc_dto = UserTelegramAccDTO(
            info=tg_acc_info,
            id=user.tg_account.id,
            phone_number=user.tg_account.phone_number,
            created_at=user.tg_account.created_at,
            api_id=user.tg_account.api_id,
        )
    return UserExtendedDTO(
        **UserDTO.model_validate(user).model_dump(), tg=user_tg_acc_dto
    )


@router.post(
    "/logout",
    dependencies=[Depends(get_user_id_or_raise)],
)
async def logout(resp: Response):
    resp.delete_cookie(AUTH_TOKEN_KEY, **cookie_attrs)


@router.get("/is-authenticated")
async def check_is_authenticated(
    user_id: Annotated[int | None, Depends(get_user_id_or_none)],
):
    return {"is_authenticated": user_id is not None}
