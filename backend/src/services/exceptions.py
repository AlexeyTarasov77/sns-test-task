from core.exceptions import BaseError


class ServiceError(BaseError):
    msg: str = "server error"


class InvalidAuthCredentialsError(ServiceError):
    msg = "invalid auth credentials"


class NotActiveUserError(ServiceError):
    msg = "user is not activated"


class UserAlreadyExistsError(ServiceError):
    msg = "user with provided username or phone number already exists"


class InvalidTelegramAccCredentialsError(ServiceError):
    msg = "invalid tg credentials"


class TelegramAccAlreadyConnectedError(ServiceError):
    msg = "you already have connected telegram to your account"
