from sanic import Sanic

from rainmq.http.message import *


def init_router(app: Sanic) -> None:
    app.add_route(produce_message, '/publish', methods=['GET', 'POST'])
    app.add_route(bring_message, '/bring', methods=['GET'])
