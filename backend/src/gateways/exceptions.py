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


class TelegramPasswordRequiredError(GatewayError):
    msg = "Your account has 2fa enabled, you must provide password to sign in"


class TelegramInvalidPhoneCodeError(GatewayError):
    msg = "Entered phone code is invalid or expired"


class TelegramInvalidPhoneNumberError(GatewayError):
    msg = "The phone number is invalid"


class TelegramInvalidCredentialsError(GatewayError):
    msg = "Provided api_id or api_hash are not valid"
