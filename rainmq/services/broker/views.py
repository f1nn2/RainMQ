from dacite import from_dict

from rainmq.entities.message import Message
from rainmq.exceptions import (
    BlockedByQueueException, EmptyQueueException
)
from rainmq.services.broker import Broker


async def produce_message(requested_payload: dict, broker: Broker) -> None:
    msg = from_dict(data_class=Message, data=requested_payload)

    broker.push(msg)


async def bring_message(requester: str, broker: Broker) -> Message:
    try:
        if is_message_owner(requester, broker.get_front()):
            return broker.bring()
        else:
            raise BlockedByQueueException
    except IndexError:
        raise EmptyQueueException


def is_message_owner(requester: str, front_msg: Message) -> bool:
    return front_msg.consumer_url == requester
