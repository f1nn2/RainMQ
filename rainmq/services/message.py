from typing import Type

from dacite import from_dict

from rainmq.entities.message import Message
from rainmq.exceptions import (
    EmptyQueueException
)
from rainmq.services.broker import Broker


async def produce_message(
    requested_payload: dict, broker: Type[Broker]
) -> None:
    msg = from_dict(data_class=Message, data=requested_payload)

    await broker.push(msg)


async def bring_message(broker: Type[Broker]) -> Message:
    try:
        return await broker.bring()
    except IndexError:
        raise EmptyQueueException
