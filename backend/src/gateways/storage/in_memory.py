from typing import Any
from gateways.contracts import IKeyValueStorage
from gateways.exceptions import StorageNotFoundError


class InMemoryStorage(IKeyValueStorage):
    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    async def get(self, key: str) -> Any:
        print("GETTING", key, self._data)
        try:
            return self._data[key]
        except KeyError:
            raise StorageNotFoundError()

    async def set(self, key: str, value: Any) -> None:
        print("SETTING", key, value)
        self._data[key] = value

    async def delete(self, key: str) -> None:
        try:
            del self._data[key]
        except KeyError:
            raise StorageNotFoundError()
