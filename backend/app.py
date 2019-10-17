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

from utils import init_background_images, iter_background_images
from config import DBG, DEFAULT_LESSONS_PAGE

app = Flask(__name__)
CORS(app)

SCRIPT_DIR = dirname(realpath(__file__))


if DBG:
    TEMP_JSON_RESULT_LIST_LESSONS = load(open(join(SCRIPT_DIR, 'temp.json')))

regexes = {
    'lblSubject': re.compile('.*_lblSubject'),
    'lblRabi': re.compile('.*_lblRabi'),
    'hlName': re.compile('.*hlName'),
    'hlSerieName': re.compile('.*_hlSerieName'),
    'lblDate': re.compile('.*_lblDate'),
    'lbllength': re.compile('.*_lbllength'),
    'hlVideo': re.compile('.*_hlVideo'),
    'hlAudio': re.compile('.*_hlAudio'),

}


def jsonified(data):
    try:
        return loads(data)
    except:
        return ''


@app.route('/backgroundPicture', methods=['GET'])
def get_background_picture():
    for pic in iter_background_images():
        return pic


@app.route('/fetch', methods=['GET'])
def fetch_lectures_from_page():
    # logging.info('str(request.data) -> ' + str(request.data))
    def get_list_lessons(url):
        list_lectures = []
        html_soup = BeautifulSoup(response.text, 'html.parser')
        tables = html_soup.find_all('table', class_='tableClass2')
        table = tables[0]
        trs = table.find_all('tr')[1:]
        tr = trs[0]
        for index, tr in enumerate(trs):
            lecure = {}
            tds = tr.find_all('td', class_='row')
            # tds = [td for td in tds if 'hiddenCol' not in str(td)]
            lecure['subject'] = getattr(
                tr.find("span", {"id": regexes['lblSubject']}), 'text', '')
            lecure['rabi'] = getattr(
                tr.find("span", {"id": regexes['lblRabi']}), 'text', '')
            lecure['name'] = getattr(
                tr.find("a", {"id": regexes['hlName']}), 'text', '')
            lecure['serieName'] = getattr(
                tr.find("a", {"id": regexes['hlSerieName']}), 'text', '')
            lecure['date'] = getattr(
                tr.find("span", {"id": regexes['lblDate']}), 'text', '')
            lecure['length'] = getattr(
                tr.find("span", {"id": regexes['lbllength']}), 'text', '')
            link_video = tr.find("a", {"id": regexes['hlVideo']})
            lecure['videoLink'] = '' if not link_video else link_video.attrs['href']
            link_audio = tr.find("a", {"id": regexes['hlAudio']})
            lecure['audioLink'] = '' if not link_audio else link_audio.attrs['href']

            list_lectures.append(lecure)

        return list_lectures
    url = request.args.get('url')
    if not url:
        return mandatory_query_args_error_response('url')
    if DBG:
        return jsonify(TEMP_JSON_RESULT_LIST_LESSONS)
    try:
        response = requests.get(url)
        if not response.ok:
            return jsonify(status="Error", url=url, msg="Error. Invalid URL")
    except:
        return jsonify(status="Error", url=url, msg="Error. Invalid URL")

    logging.info("req -> url : '%s'" % url)
    list_lectures = get_list_lessons(url)
    if not list_lectures:
        get_list_lessons(DEFAULT_LESSONS_PAGE)
    logging.info("[Response-Jsonify] return %s Lectures..." %
                 len(list_lectures))
    # DBG:
    # dump(list_lectures, open(join(SCRIPT_DIR, 'temp.json'), 'wb'))
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
        logging.error("Error. Invalid Format. data -> " + str(request.data))
        return mandatory_query_args_error_response('url')

    if not url_ok(url):
        print ("[downloadFile] Invalid URL '%s'" % url)

    req_file = requests.get(url, stream=True)
    return Response(stream_with_context(req_file.iter_content(chunk_size=4096)), content_type=req_file.headers['content-type'])


def url_ok(url):
    r = requests.head(url)
    return r.status_code == 200


def init_logging():
    handlers = [logging.StreamHandler()]
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)-5.5s] %(message)s',
        handlers=handlers
    )


def has_args_keys(list_query_keys):
    if not isinstance(list_query_keys, list):
        list_query_keys = [list_query_keys]
    for key in list_query_keys:
        if key not in request.args:
            return False
    return True


def mandatory_query_args_error_response(mandatory_keys, **kargs):
    logging.error("Error. Invalid Format. data -> " + str(request.data))
    response = jsonify(status="Error", data=request.data,
                       msg="mandatory query keys: %s" % mandatory_keys, **kargs)
    response.status_code = 400
    return response


if __name__ == '__main__':
    init_logging()
    init_background_images()
    # app.run(host='127.0.0.1', port=8000, debug=True)
    app.run(host='127.0.0.1', port=8000)
