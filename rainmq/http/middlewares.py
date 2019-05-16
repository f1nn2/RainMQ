from sanic.exceptions import NotFound
from sanic.response import HTTPResponse
from sanic.request import Request

from rainmq.http.broker import SingleQueueBroker


async def set_security_headers(
    request: Request,
    response: HTTPResponse
) -> HTTPResponse:
    try:
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'deny'
    finally:
        return response


async def no_contents_handler(
    request: Request, exception
) -> HTTPResponse:
    return HTTPResponse(body=None, status=204)


async def not_found_handler(
    request: Request, exception
) -> NotFound:
    raise NotFound


async def initialize(app, loop):
    await SingleQueueBroker.initialize()
