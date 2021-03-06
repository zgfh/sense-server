from flask import Blueprint, abort, g

from sense_server.app import app

import api

api_version = "v1"
route_prefix = "/api/{version}".format(version=api_version)

API = Blueprint("api", __name__, url_prefix=route_prefix)

routes = (

    (['GET'], "/ping", api.ping),
    (['GET'], "/posts", api.list_post_api),
    (['PUT'], "/posts/<id>/read", api.read_post_api),
    (['POST'], "/posts/read", api.read_posts_api),
    (['POST'], "/posts/unread", api.unread_posts_api),
    (['PUT'], "/posts/<id>/unread", api.unread_post_api),
    (['GET'], "/favorites", api.list_favorites_api),
    (['POST'], "/favorites", api.add_favorites_api),
    (['DELETE'], "/favorites", api.remove_favorites_api),

)


def register_route():
    for route in routes:
        API.add_url_rule(route[1], view_func=route[2], methods=route[0])


register_route()
app.register_blueprint(API)
