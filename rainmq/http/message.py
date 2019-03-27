from datetime import datetime
from uuid import uuid4

from sanic.request import Request
from sanic.response import json, HTTPResponse

from rainmq.services.broker import views


async def produce_message(request: Request) -> HTTPResponse:
    msg = await views.produce_message(
        split_params(request), request.app.broker
    )

    return json({'inserted_message': msg}, 200)


def split_params(request: Request) -> dict:
    headers = dict(request.headers)

    return {
        'id': str(uuid4()).replace('-', ''),
        'producer_url': f"{request.ip}:{request.port}",
        'consumer_url': headers.pop('x-origin-receiver'),
        'original_method': request.method,
        'headers': headers,
        'query_str': request.query_string or None,
        'json': request.json or None,
        'inserted_at': datetime.utcnow()
    }


# Todo (temp check func. To be deleted)
async def check_queue(request: Request):
    print(request.app.broker._q1._queue)
    return json({'current_queue': request.app.broker._q1._queue}, 200)
