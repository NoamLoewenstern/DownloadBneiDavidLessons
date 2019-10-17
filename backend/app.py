from os.path import dirname, realpath, join, exists, basename
from os import remove
from json import load, dump, loads, dumps
import re
from time import sleep
import httplib
import logging

from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, Response, abort, request, stream_with_context
from flask_cors import CORS

from utils import jsonified, init_background_images, iter_background_images
from config import DBG, TEMP_JSON_RESULT_LIST_LESSONS, DEFAULT_LESSONS_PAGE
from requests_utils import get_list_lessons

SCRIPT_DIR = dirname(realpath(__file__))
app = Flask(__name__, static_url_path='build')
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('buil')


@app.route('/backgroundPicture', methods=['GET'])
def get_background_picture():
    for pic in iter_background_images():
        return pic


@app.route('/fetch', methods=['GET'])
def fetch_lectures_from_page():
    # logging.info('str(request.data) -> ' + str(request.data))

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


@app.route('/downloadFile', methods=['GET'])
def downloadFile():
    def generate_stream_data(url):
        req_file = requests.get(url, stream=True)
        # print ("[downloadFile] downloading '%s'" % url)
        # dbg_filename = join(SCRIPT_DIR, 'temp_files', "tempFile.mp3")
        # if exists(dbg_filename):
        #     print("removing '%s'" % basename(dbg_filename))
        #     remove(dbg_filename)
        #     sleep(1)
        # print("[downloadFile] saving file to '%s'" % basename(dbg_filename))
        #     for chunk in req_file.iter_content(chunk_size=64000):
        #         fh.write(chunk)
        # with open(dbg_filename, 'ab') as fh:
        #     for chunk in req_file.iter_content(chunk_size=1024):
        #         fh.write(chunk)
        #         yield str(chunk)
        # print("[downloadFile] Finished Saving.. '%s'" % basename(dbg_filename))
        for chunk in req_file.iter_content(chunk_size=4096):
            yield str(chunk)

    url = request.args.get('url')
    if not url:
        logging.error("Error. Invalid Format. data -> %s" % request.data)
        return mandatory_query_args_error_response('url')

    if not url_ok(url):
        print ("[downloadFile] Invalid URL '%s'" % url)

    req_file = requests.get(url, stream=True)
    return Response(stream_with_context(req_file.iter_content(chunk_size=4096)), content_type=req_file.headers['content-type'])


def url_ok(url):
    r = requests.head(url)
    return r.status_code == 200


def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format='%(asctime)s [%(levelname)-5.5s] %(message)s',
        handlers=[
            # logging.FileHandler("{}/{}".format(log_path, log_name)),
            logging.StreamHandler()
        ]
    )


def has_args_keys(list_query_keys):
    if not isinstance(list_query_keys, list):
        list_query_keys = [list_query_keys]
    for key in list_query_keys:
        if key not in request.args:
            return False
    return True


def mandatory_query_args_error_response(mandatory_keys, **kargs):
    logging.error("Error. Invalid Format. data -> {}".format(request.data))
    response = jsonify(status="Error", data=request.data,
                       msg="mandatory query keys: %s" % mandatory_keys, **kargs)
    response.status_code = 400
    return response


if __name__ == '__main__':
    init_logging()
    init_background_images()
    # app.run(host='127.0.0.1', port=8000, debug=True)
    app.run(host='127.0.0.1', port=8000)
