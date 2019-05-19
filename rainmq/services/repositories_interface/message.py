from abc import ABC, abstractmethod


class MessageRepository(ABC):
    @abstractmethod
    async def log(self, message: dict):
        pass

    @abstractmethod
    async def delete(self, message_id: str):
        # no real delete, update status
        pass
