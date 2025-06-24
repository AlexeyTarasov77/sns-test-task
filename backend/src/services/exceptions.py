from core.exceptions import BaseError


class ServiceError(BaseError):
    msg: str = "server error"
