from sanic.response import HTTPResponse
from sanic.request import Request


async def set_security_headers(
    request: Request,
    response: HTTPResponse
) -> HTTPResponse:
    try:
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'deny'
    finally:
        return response


async def queue_exception_handler(
    request: Request, exception
) -> HTTPResponse:
    return HTTPResponse(body=None, status=204)
