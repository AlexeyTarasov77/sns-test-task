from dto.base import BaseDTO
from pydantic import Field


class UserDTO(BaseDTO):
    id: int
    username: str
    phone_number: str


class SignInDTO(BaseDTO):
    username: str
    password: str = Field(min_length=8)


class SignInResultDTO(BaseDTO):
    user: UserDTO
    token: str


# TODO: add proper phone number validation
class SignUpDTO(SignInDTO):
    phone_number: str
