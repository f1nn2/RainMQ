from sanic import Sanic
from sanic.request import Request
from sanic.response import text

from rainmq.conf import Config, Testing, Development, Production
from rainmq.http import init_router
from rainmq.http.middlewares import (
    set_security_headers,
    no_contents_handler,
    not_found_handler,
    initialize,
)
from rainmq.exceptions import (
    EmptyQueueException,
    TopicNotFoundException
)


BEFORE_SERVER_START = 'before_server_start'
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
    app.register_listener(initialize, BEFORE_SERVER_START)

    app.register_middleware(set_security_headers, BEFORE_RESPONSE)

    app.error_handler.add(EmptyQueueException, no_contents_handler)
    app.error_handler.add(TopicNotFoundException, not_found_handler)


def create_app() -> Sanic:
    app_ = Sanic(__name__)

    app_.config.from_object(init_config())
    init_middleware(app_)
    init_router(app_)

    @app_.route('/')
    async def ping(_: Request):
        return text(PING, 200)

    return app_
