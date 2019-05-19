from typing import Type
from dataclasses import asdict

from dacite import from_dict

from rainmq.entities.message import Message
from rainmq.exceptions import (
    EmptyQueueException,
    TopicNotFoundException,
)
from rainmq.http.broker import Broker
from rainmq.services.repositories_interface.message import MessageRepository


async def produce_message(
    requested_payload: dict,
    broker: Type[Broker],
    topic_name: str,
    repo: MessageRepository
) -> None:
    msg = from_dict(data_class=Message, data=requested_payload)

    await broker.push(msg, topic_name)
    await repo.log(asdict(msg))


async def bring_message(
    broker: Type[Broker], topic_name: str, repo: MessageRepository
) -> Message:
    try:
        brought_message = await broker.bring(topic_name)
    except IndexError:
        raise EmptyQueueException
    except KeyError:
        raise TopicNotFoundException
    else:
        await repo.delete(brought_message.id)

    return brought_message
