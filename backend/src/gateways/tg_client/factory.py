from models import TelegramAccount
from .provider import TelethonTgProvider
from gateways.contracts import ITelegramClient, ITelegramClientFactory


class TelethonTgClientFactory(ITelegramClientFactory):
    def new_client(self, acc: TelegramAccount) -> ITelegramClient:
        return TelethonTgProvider(acc)
