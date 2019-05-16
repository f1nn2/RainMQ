from abc import ABC, abstractmethod
from collections import deque
from typing import Dict


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
    async def push(cls, message: Message, topic_name: str):
        ...

    @classmethod
    @abstractmethod
    async def bring(cls, topic_name: str) -> Message:
        ...


class OneQueueTopicBroker(Broker):
    __topics: Dict[str, MessageQueue] = {}

    @classmethod
    async def initialize(cls):
        ...

    @classmethod
    async def _create_topic(cls, topic_name: str) -> MessageQueue:
        cls.__topics[topic_name] = MessageQueue()
        return cls.__topics[topic_name]

    @classmethod
    async def push(cls, message: Message, topic_name: str):
        topic: MessageQueue
        try:
            topic = cls.__topics[topic_name]
        except KeyError:
            topic = await cls._create_topic(topic_name)
        finally:
            await topic._push(message)

    @classmethod
    async def bring(cls, topic_name: str) -> Message:
        try:
            return await cls.__topics[topic_name]._pop()
        except (KeyError, IndexError) as exc:
            raise exc


class SingleQueueBroker:
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

