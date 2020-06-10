from http import HTTPStatus
from flask import Response
import json


def make_json_response(data: dict,
                       status_code=200,
                       headers: dict = None) -> Response:

    res = Response(json.dumps(data),
                   status=HTTPStatus.OK,
                   mimetype='application/json')

    if headers:
        for header, val in headers.items():
            res.headers[header] = val

    return res
