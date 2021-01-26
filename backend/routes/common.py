import logging
from flask import request, jsonify
import requests


def mandatory_query_args_error_response(mandatory_keys, **kargs):
    logging.error(f"Invalid Query argements. Missing Keys: {mandatory_keys}")
    response = jsonify(
        status="Error",
        data=str(request.data, "utf8"),
        msg=f"mandatory query keys: {mandatory_keys}",
        # **kargs,
    )
    response.status_code = 400
    return response


def url_exists(url):
    r = requests.head(url)
    return r.status_code == 200


def has_args_keys(list_query_keys):
    if not isinstance(list_query_keys, list):
        list_query_keys = [list_query_keys]
    for key in list_query_keys:
        if key not in request.args:
            return False
    return True
