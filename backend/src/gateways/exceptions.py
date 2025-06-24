from core.exceptions import BaseError


class GatewayError(BaseError):
    msg = "gateway error"


class StorageNotFoundError(GatewayError):
    msg = "record not found in storage"


class StorageAlreadyExistsError(GatewayError):
    msg = "record already exists"


class StorageInvalidRefError(GatewayError):
    """Raised in case of fk violation"""

    msg = "Invalid reference"
