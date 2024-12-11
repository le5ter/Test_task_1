from settings import POSTGRES_CONNECTION_STRING_ASYNC

from .base import AsyncPostgreSQLClient


class PGManager:
    def __init__(self, echo: bool = False) -> None:
        self.client = AsyncPostgreSQLClient(POSTGRES_CONNECTION_STRING_ASYNC, echo)
