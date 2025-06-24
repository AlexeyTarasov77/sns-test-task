from datetime import timedelta
from gateways.contracts import IJwtTokenProvider, IPasswordHasher, IUsersRepo
from dto import SignInDTO
from gateways.exceptions import StorageNotFoundError
from services.exceptions import InvalidCredentialsError, NotActiveUserError
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
        self._auth_token_ttl = auth_token_ttl

    async def signin(self, dto: SignInDTO) -> tuple[User, str]:
        try:
            user = await self._users_repo.get_by_username(dto.username)
        except StorageNotFoundError as e:
            raise InvalidCredentialsError() from e
        if not user.is_active:
            raise NotActiveUserError()
        if not self._password_hasher.compare(dto.password, user.password_hash):
            raise InvalidCredentialsError()
        token = self._jwt_token_provider.new_token(
            {"uid": user.id}, self._auth_token_ttl
        )
        return user, token
