from sanic import Sanic

from .message import *


def init_router(app: Sanic) -> None:
    app.add_route(produce_message, '/publish', methods=['GET', 'POST'])
    app.add_route(bring_message, '/bring', methods=['GET'])

    # Todo (temp check router. To be deleted)
    app.add_route(check_queue, '/check', methods=['GET'])
