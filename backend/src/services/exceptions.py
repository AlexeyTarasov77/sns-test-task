from core.exceptions import BaseError


class ServiceError(BaseError):
    msg: str = "server error"


class InvalidCredentialsError(ServiceError):
    msg = "invalid credentials"


class NotActiveUserError(ServiceError):
    msg = "user is not activated"
