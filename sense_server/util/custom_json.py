import json

import datetime
from sense_server.util._time import datetime_to_iso_format


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return datetime_to_iso_format(obj)
        return json.JSONEncoder.default(self, obj)


def dthandler(obj):
    if isinstance(obj, datetime.datetime):
        return datetime_to_iso_format(obj)
    else:
        return None
