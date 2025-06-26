from datetime import datetime
from dto.base import BaseDTO
from pydantic import Field

from dto.telegram import TelegramAccountInfoDTO


class UserDTO(BaseDTO):
    id: int
    username: str
    phone_number: str


class UserTelegramAccDTO(BaseDTO):
    id: int
    api_id: int
    phone_number: str
    created_at: datetime
    info: TelegramAccountInfoDTO


class UserExtendedDTO(UserDTO):
    tg: UserTelegramAccDTO | None = None


class SignInDTO(BaseDTO):
    username: str
    password: str = Field(min_length=8)


class SignInResultDTO(BaseDTO):
    user: UserDTO
    token: str


# TODO: add proper phone number validation
class SignUpDTO(SignInDTO):
    phone_number: str
