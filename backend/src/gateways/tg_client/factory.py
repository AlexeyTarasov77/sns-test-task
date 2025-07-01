from models import TelegramAccount
from .provider import TelethonTgProvider
from gateways.contracts import ITelegramClient, ITelegramClientFactory


class TelethonTgClientFactory(ITelegramClientFactory):
    def __init__(self):
        self._cached_clients: dict[int, ITelegramClient] = {}

    def new_client(self, acc: TelegramAccount) -> ITelegramClient:
        cached_client = self._cached_clients.get(acc.id)
        if not cached_client:
            new_client = TelethonTgProvider(acc)
            self._cached_clients[acc.id] = new_client
            return new_client
        return cached_client
