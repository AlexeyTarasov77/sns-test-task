from collections.abc import Mapping
from fastapi import FastAPI, Request, status
from logging import Logger
from fastapi.responses import JSONResponse
from services import exceptions as service_exc


class HTTPExceptionsMapper:
    """Maps service errors to corresponding http status code"""

    _EXCEPTION_MAPPING: Mapping[type[Exception], int] = {
        service_exc.InvalidAuthCredentialsError: status.HTTP_401_UNAUTHORIZED,
        service_exc.NotActiveUserError: status.HTTP_400_BAD_REQUEST,
        service_exc.InvalidConfirmationCodeError: status.HTTP_400_BAD_REQUEST,
        service_exc.InvalidTelegramAccCredentialsError: status.HTTP_400_BAD_REQUEST,
        service_exc.TelegramAcc2FARequired: status.HTTP_403_FORBIDDEN,
        service_exc.TelegramAccNotConnectedError: status.HTTP_404_NOT_FOUND,
        service_exc.UserAlreadyExistsError: status.HTTP_409_CONFLICT,
        service_exc.TelegramAccAlreadyConnectedError: status.HTTP_409_CONFLICT,
        service_exc.UserAlreadyExistsError: status.HTTP_409_CONFLICT,
    }

    def __init__(
        self,
        app: FastAPI,
        logger: Logger,
    ):
        self._app = app
        self._logger = logger

    async def _handle(self, _: Request, exc: Exception):
        status_code: int | None = self._EXCEPTION_MAPPING.get(type(exc), None)
        if status_code is None:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            self._logger.error("Unknown exception in handler: %s", exc, exc_info=True)
        message: str = str(exc) if status_code < 500 else "Internal server error."
        return JSONResponse({"detail": message}, status_code)

    def setup_handlers(self) -> None:
        for exc_class in self._EXCEPTION_MAPPING:
            self._app.add_exception_handler(exc_class, self._handle)
        self._app.add_exception_handler(Exception, self._handle)
