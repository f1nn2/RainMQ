from datetime import datetime
from uuid import uuid4

from sanic.request import Request
from sanic.response import HTTPResponse, json

from rainmq.services.broker import SingleQueueBroker
from rainmq.services import message as service


async def produce_message(request: Request) -> HTTPResponse:
    await service.produce_message(
        split_params(request), SingleQueueBroker
    )

    return HTTPResponse(status=201)


async def bring_message(request: Request) -> HTTPResponse:
    msg = await service.bring_message(SingleQueueBroker)

    return json({'brought_message': msg}, 200)


def split_params(request: Request) -> dict:
    headers = dict(request.headers)

    return {
        'id': str(uuid4()).replace('-', ''),
        'producer_url': f"{request.ip}:{request.port}",
        'http_method': request.method,
        'headers': headers,
        'query_str': request.query_string or None,
        'json': request.json or None,
        'inserted_at': datetime.utcnow()
    }
