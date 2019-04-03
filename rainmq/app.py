from sanic import Sanic
from sanic.request import Request
from sanic.response import text, HTTPResponse

from rainmq.conf import Config, Testing, Development, Production
from rainmq.http import init_router
from rainmq.http.middlewares import (
    set_security_headers,
    queue_exception_handler,
)
from rainmq.services.broker import Broker
from rainmq.exceptions import (
    BlockedByQueueException,
    EmptyQueueException,
)


BEFORE_RESPONSE = 'response'
PING = 'ping'


def init_config(env: str = 'default') -> Config:
    mapping = {
        'default': Config,
        'testing': Testing,
        'development': Development,
        'production': Production,
    }
    config = mapping[env](env=env)
    check_env_type(config)

    return config


def check_env_type(config: Config):
    if config.env == 'production' and config.DEBUG:
        raise RuntimeError('You should set DEBUG to false in production')


def init_middleware(app: Sanic) -> None:
    app.register_middleware(set_security_headers, BEFORE_RESPONSE)

    app.error_handler.add(EmptyQueueException, queue_exception_handler)
    app.error_handler.add(BlockedByQueueException, queue_exception_handler)


def create_broker(app: Sanic) -> None:
    app.broker = Broker()


def create_app() -> Sanic:
    app_ = Sanic(__name__)

    app_.config.from_object(init_config())
    init_middleware(app_)
    init_router(app_)
    create_broker(app_)

    @app_.route('/')
    async def ping(_: Request):
        return text(PING, 200)

    return app_
