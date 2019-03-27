from dacite import from_dict

from rainmq.entities.message import Message
from rainmq.services.broker import Broker


async def produce_message(requested_payload: dict, broker: Broker) -> Message:
    msg = from_dict(data_class=Message, data=requested_payload)

    broker.push_into_queue(msg)

    return msg
