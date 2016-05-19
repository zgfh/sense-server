import json

from flask import Flask, Response, request

from flask_cors import CORS
from sense_server.util.custom_json import dthandler

app = Flask("api")

app.config['CORS_MAX_AGE'] = 86400
cors = CORS(app)


def json_resp(data, headers=None):
    return Response(json.dumps(data, indent=4, default=dthandler), mimetype='application/json', headers=headers)


@app.route('/ping')
def show_ping():
    return "PONG"


@app.before_request
def merge_json():
    json = request.get_json(silent=True)
    if json:
        import werkzeug.datastructures

        request.values = werkzeug.datastructures.CombinedMultiDict([request.args, request.form, json])
