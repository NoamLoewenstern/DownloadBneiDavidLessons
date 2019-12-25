import logging

import requests
from flask import Blueprint, jsonify, Response, request, stream_with_context

from .config import (
    DBG,
    TEMP_JSON_RESULT_LIST_LESSONS,
    DEFAULT_LESSONS_PAGE,
)
from .common import mandatory_query_args_error_response, url_exists
from .bd_requests import BneiDavidWebsiteRequests as BDRequests

BACKGROUND_IMAGES_ITER = BDRequests.iter_background_images()

api_routes = Blueprint("api_routes", __name__,)


@api_routes.route("/backgroundImage", methods=["GET"])
def get_background_image():
    return Response(next(BACKGROUND_IMAGES_ITER))


@api_routes.route("/fetch", methods=["GET"])
def fetch_lessons_from_page():
    url = request.args.get("url")
    if not url:
        return mandatory_query_args_error_response("url")
    if DBG:
        return jsonify(TEMP_JSON_RESULT_LIST_LESSONS)

    # logging.info(f"req: {url}")
    success, list_lessons = BDRequests.get_list_lessons(url)
    if not success:
        return list_lessons
    if len(list_lessons) == 0:
        success, list_lessons = BDRequests.get_list_lessons(DEFAULT_LESSONS_PAGE)
        if not success:
            return list_lessons
    # logging.info(f"returned {len(list_lessons)} lessons.")
    return jsonify(list_lessons)


@api_routes.route("/downloadFile", methods=["GET"])
def downloadFile():
    def generate_stream_data(url):
        req_file = requests.get(url, stream=True)
        for chunk in req_file.iter_content(chunk_size=4096):
            yield str(chunk)

    url = request.args.get("url")
    if not url:
        logging.error(f"Invalid Format. url: {url}")
        return mandatory_query_args_error_response("url")

    if not url_exists(url):
        print(f"[downloadFile] Invalid URL {url}")

    req_file = requests.get(url, stream=True)
    return Response(
        stream_with_context(req_file.iter_content(chunk_size=4096)),
        content_type=req_file.headers["content-type"],
    )
