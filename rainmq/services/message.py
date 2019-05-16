from typing import Type

from dacite import from_dict

from rainmq.entities.message import Message
from rainmq.exceptions import (
    EmptyQueueException,
    TopicNotFoundException,
)
from rainmq.http.broker import Broker


async def produce_message(
    requested_payload: dict, broker: Type[Broker], topic_name: str
) -> None:
    msg = from_dict(data_class=Message, data=requested_payload)

    await broker.push(msg, topic_name)


async def bring_message(broker: Type[Broker], topic_name: str) -> Message:
    try:
        return await broker.bring(topic_name)
    except IndexError:
        raise EmptyQueueException
    except KeyError:
        raise TopicNotFoundException
