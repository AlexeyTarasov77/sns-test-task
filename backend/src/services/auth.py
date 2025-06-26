from datetime import datetime, timedelta
from jwt.exceptions import InvalidTokenError as InvalidJwtTokenError
from typing import Any
from gateways.contracts import IJwtTokenProvider, IPasswordHasher, IUsersRepo
from dto import SignInDTO, SignUpDTO, SignInResultDTO
from gateways.exceptions import StorageAlreadyExistsError, StorageNotFoundError
from services.exceptions import (
    InvalidAuthCredentialsError,
    InvalidAuthTokenError,
    NotActiveUserError,
    UserAlreadyExistsError,
)
from models.user import User


class AuthService:
    def __init__(
        self,
        users_repo: IUsersRepo,
        password_hasher: IPasswordHasher,
        jwt_token_provider: IJwtTokenProvider,
        auth_token_ttl: timedelta,
    ):
        self._users_repo = users_repo
        self._password_hasher = password_hasher
        self._jwt_token_provider = jwt_token_provider
        self.auth_token_ttl = auth_token_ttl
        self.token_uid_key = "uid"

    async def signin(self, dto: SignInDTO) -> SignInResultDTO:
        try:
            user = await self._users_repo.get_by_username(dto.username)
        except StorageNotFoundError as e:
            raise InvalidAuthCredentialsError() from e
        if not user.is_active:
            raise NotActiveUserError()
        if not self._password_hasher.compare(dto.password, user.password_hash):
            raise InvalidAuthCredentialsError()
        token = self._jwt_token_provider.new_token(
            {self.token_uid_key: user.id}, self.auth_token_ttl
        )
        return SignInResultDTO.model_validate({"user": user, "token": token})

    async def signup(self, dto: SignUpDTO) -> User:
        password_hash = self._password_hasher.hash(dto.password)
        user = User(
            username=dto.username,
            phone_number=dto.phone_number,
            password_hash=password_hash,
        )
        try:
            return await self._users_repo.save(user)
        except StorageAlreadyExistsError:
            raise UserAlreadyExistsError()

    async def verfiy_token(self, token: str) -> dict[str, Any]:
        try:
            token_payload = self._jwt_token_provider.extract_payload(token)
            token_exp = datetime.fromtimestamp(token_payload["exp"])
        except (InvalidJwtTokenError, KeyError) as e:
            raise InvalidAuthTokenError() from e
        if token_exp < datetime.now():
            raise InvalidAuthTokenError()
        return token_payload

    async def get_current_user(self, user_id: int) -> User:
        try:
            return await self._users_repo.get_by_id(user_id)
        except StorageNotFoundError as e:
            raise InvalidAuthCredentialsError() from e
