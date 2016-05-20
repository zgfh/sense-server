import controller

from flask import request

from sense_server.app import json_resp, str2bool


def ping():
    return "pong"


def remove_favorites_api():
    ids = request.values.get("ids")
    controller.remove_favorites(ids)
    return json_resp({})


def list_post_api():
    read = str2bool(request.values.get("read"), False)

    return json_resp(controller.list_post(read=read))


def read_post_api(id):
    return json_resp(controller.read_post(id))


def unread_post_api(id):
    controller.unread_post(id)
    return json_resp({})


def list_favorites_api():
    return json_resp(controller.list_favorites())


def add_favorites_api():
    ids = request.values.get("ids")
    controller.add_favorites(ids)
    return json_resp(ids)
