from collections import deque
from abc import ABC, abstractmethod


from rainmq.entities.message import Message


class MessageQueue:
    def __init__(self):
        self._queue = deque()

    async def _push(self, message: Message):
        self._queue.append(message)

    async def _pop(self) -> Message:
        return self._queue.popleft()

    async def _get_front(self) -> Message:
        return self._queue[0]

    async def _is_empty(self) -> bool:
        return not bool(len(self._queue))


class Broker(ABC):
    @classmethod
    @abstractmethod
    async def initialize(cls):
        ...

    @classmethod
    @abstractmethod
    async def push(cls, message: Message):
        ...

    @classmethod
    @abstractmethod
    async def bring(cls) -> Message:
        ...

    @classmethod
    @abstractmethod
    async def get_front(cls) -> Message:
        ...

    @classmethod
    @abstractmethod
    async def is_empty(cls) -> bool:
        ...


class SingleQueueBroker(Broker):
    __queue: MessageQueue = None

    @classmethod
    async def initialize(cls):
        cls.__queue = MessageQueue()

    @classmethod
    async def push(cls, message: Message):
        await cls.__queue._push(message)

    @classmethod
    async def bring(cls) -> Message:
        return await cls.__queue._pop()

    @classmethod
    async def get_front(cls) -> Message:
        return await cls.__queue._get_front()

    @classmethod
    async def is_empty(cls) -> bool:
        return await cls.__queue._is_empty()

