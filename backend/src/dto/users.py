from dto.base import BaseDTO


class SignInDTO(BaseDTO):
    username: str
    password: str


# TODO: add proper phone number validation
class SignUpDTO(SignInDTO):
    phone_number: str
