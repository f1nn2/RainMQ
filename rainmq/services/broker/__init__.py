from collections import deque

from rainmq.entities.message import Message
from rainmq.exceptions import EmptyQueuePopException
from rainmq.services.utils import Singleton


class MessageQueue:
    def __init__(self):
        self._queue = deque()

    def _push(self, message: Message):
        self._queue.append(message)

    def _pop(self) -> Message:
        try:
            return self._queue.popleft()
        except IndexError:
            raise EmptyQueuePopException


class Broker(Singleton):
    def __init__(self):
        self._q1 = MessageQueue()

    def push_into_queue(self, message: Message):
        self._q1._push(message)

    def pop_from_queue(self) -> Message:
        return self._q1._pop()
