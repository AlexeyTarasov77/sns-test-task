from dto.base import BaseDTO


class TgAccountCredentialsDTO(BaseDTO):
    api_id: int
    api_hash: str
