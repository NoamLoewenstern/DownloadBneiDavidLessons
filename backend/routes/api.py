from os.path import dirname, realpath
import logging

import requests
from flask import Blueprint, jsonify, Response, request, stream_with_context

from requests_utils import get_list_lessons
from config import DBG, TEMP_JSON_RESULT_LIST_LESSONS, DEFAULT_LESSONS_PAGE
from utils import iter_background_images
from common import mandatory_query_args_error_response, url_exists

SCRIPT_DIR = dirname(realpath(__file__))

BACKGROUND_IMAGES_ITER = iter_background_images()

api_routes = Blueprint('api_routes', __name__)


@api_routes.route('/backgroundImage', methods=['GET'])
def get_background_image():
    return Response(next(BACKGROUND_IMAGES_ITER))


@api_routes.route('/fetch', methods=['GET'])
def fetch_lectures_from_page():
    url = request.args.get('url')
    if not url:
        return mandatory_query_args_error_response('url')
    if DBG:
        return jsonify(TEMP_JSON_RESULT_LIST_LESSONS)

    logging.info("req -> url : {}".format(url))
    success, list_lectures = get_list_lessons(url)
    if not success:
        return list_lectures
    if len(list_lectures) == 0:
        success, list_lectures = get_list_lessons(DEFAULT_LESSONS_PAGE)
        if not success:
            return list_lectures
    logging.info("[Response-Jsonify] return {} Lectures...".format(len(list_lectures)))
    return jsonify(list_lectures)


@api_routes.route('/downloadFile', methods=['GET'])
def downloadFile():
    def generate_stream_data(url):
        req_file = requests.get(url, stream=True)
        for chunk in req_file.iter_content(chunk_size=4096):
            yield str(chunk)

    url = request.args.get('url')
    if not url:
        logging.error("Error. Invalid Format. data -> {}".format(request.data))
        return mandatory_query_args_error_response('url')

    if not url_exists(url):
        print ("[downloadFile] Invalid URL {}".format(url))

    req_file = requests.get(url, stream=True)
    return Response(stream_with_context(req_file.iter_content(chunk_size=4096)), content_type=req_file.headers['content-type'])
