from datetime import datetime, timedelta
import jwt
from typing import Any


def _get_expiry(expires_in: timedelta) -> datetime:
    if expires_in.total_seconds() == 0:
        raise ValueError("Invalid expiration")
    return datetime.now() + expires_in


class JwtTokenProvider:
    def __init__(self, secret_key: str, signing_alg: str = "HS256") -> None:
        self._secret = secret_key
        self.alg = signing_alg

    def new_token(self, payload: dict[str, Any], expires_in: timedelta) -> str:
        payload["exp"] = _get_expiry(expires_in)
        return jwt.encode(payload, self._secret, self.alg)

    def extract_payload(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, self._secret, [self.alg])
