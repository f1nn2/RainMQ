from sanic import Sanic

from rainmq.http.message import *


def init_router(app: Sanic) -> None:
    app.add_route(
        produce_message, '/<topic_name>/publish', methods=['GET', 'POST']
    )
    app.add_route(bring_message, '/<topic_name>/bring', methods=['GET'])
