from dto.base import BaseDTO
from pydantic import Field


class SignInDTO(BaseDTO):
    username: str
    password: str = Field(min_length=8)


# TODO: add proper phone number validation
class SignUpDTO(SignInDTO):
    phone_number: str
