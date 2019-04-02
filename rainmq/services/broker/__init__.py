from collections import deque

from rainmq.entities.message import Message
from rainmq.services.utils import Singleton


class MessageQueue:
    def __init__(self):
        self._queue = deque()

    def _push(self, message: Message):
        self._queue.append(message)

    def _pop(self) -> Message:
        return self._queue.popleft()

    def _get_front(self) -> Message:
        return self._queue[0]

    def _is_empty(self) -> bool:
        return not bool(len(self._queue))


class Broker(Singleton):
    def __init__(self):
        self._q1 = MessageQueue()

    def push(self, message: Message):
        self._q1._push(message)

    def bring(self) -> Message:
        return self._q1._pop()

    def get_front(self) -> Message:
        return self._q1._get_front()

    def is_empty(self) -> bool:
        return self._q1._is_empty()
