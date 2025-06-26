from core.exceptions import BaseError


class ServiceError(BaseError):
    msg: str = "server error"


class InvalidAuthTokenError(ServiceError):
    msg = "invalid or expired auth token. Try to sign in again"


class InvalidAuthCredentialsError(ServiceError):
    msg = "invalid auth credentials"


class NotActiveUserError(ServiceError):
    msg = "user is not activated"


class UserAlreadyExistsError(ServiceError):
    msg = "user with provided username or phone number already exists"


class InvalidTelegramAccCredentialsError(ServiceError):
    msg = "invalid tg credentials"


class InvalidConfirmationCodeError(ServiceError):
    msg = "Provided confirmation code is invalid or expired"


class ChatNotFoundError(ServiceError):
    msg = "chat with given id does not exist"


class TelegramAccNotExistError(ServiceError):
    msg = "telegram account with provided phone number does not exist"


class TelegramAccNotConnectedError(ServiceError):
    msg = "you don't have connected telegram account"


class TelegramAccAlreadyConnectedError(ServiceError):
    msg = "you already have connected telegram to your account"


class TelegramAcc2FARequired(ServiceError):
    msg = "You have two factor authentication turned on, so you should supply additional password to sign in"
