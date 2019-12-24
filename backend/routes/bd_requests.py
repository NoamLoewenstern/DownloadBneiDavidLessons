import os
from os.path import join, dirname, realpath
import re
import requests
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from flask import jsonify
from bs4 import BeautifulSoup
from threading import Thread
from .config import BASE_BNEI_URL, BACKGROUND_IMAGES_LINKS
from .helpers import hash_dict


re_fetch_bg_image = re.compile(r"background:url\((?P<image>.+?)\)")
LESSONS_PATTERNS = {
    "lblSubject": re.compile(r".*_lblSubject"),
    "lblRabi": re.compile(r".*_lblRabi"),
    "hlName": re.compile(r".*hlName"),
    "hlSerieName": re.compile(r".*_hlSerieName"),
    "lblDate": re.compile(r".*_lblDate"),
    "lbllength": re.compile(r".*_lbllength"),
    "hlVideo": re.compile(r".*_hlVideo"),
    "hlAudio": re.compile(r".*_hlAudio"),
}

CACHE_RESP_DIR = realpath(join(dirname(__file__), "..", "cache_responses"))
MAX_REFRESH_CACHE = 60 * 30  # 30 min


class BneiDavidWebsiteRequests:
    BACKGROUND_IMAGES = []

    def __init(self):
        pass

    @classmethod
    def get_list_lessons(cls, url):
        list_in_cache = cls.get_cached_lessons(url)
        if list_in_cache:
            return True, list_in_cache
        try:
            response = requests.get(url)
        except requests.exceptions.MissingSchema:
            return False, jsonify(status="Error", url=url, msg="Invalid URL Schema")
        except requests.exceptions.ConnectionError:
            return (
                False,
                jsonify(
                    status="Error",
                    url=url,
                    msg=f"Failed to establish a connection with {url}",
                ),
            )
        else:
            if not response.ok:
                return False, jsonify(status="Error", url=url, msg="Invalid URL")
            list_lessons = []
            html_soup = BeautifulSoup(response.text, "html.parser")
            tables = html_soup.find_all('table', {'class': ['tableClass', 'tableClass2']})
            for table in tables:
                trs = table.find_all("tr")[1:]
                tr = trs[0]
                for index, tr in enumerate(trs):
                    lecure = {}
                    # tds = tr.find_all("td", class_="row")
                    # tds = [td for td in tds if 'hiddenCol' not in str(td)]
                    lecure['subject'] = getattr(
                        tr.find("span", {'id': LESSONS_PATTERNS['lblSubject']}), 'text', ''
                    )
                    lecure['rabi'] = getattr(
                        tr.find("span", {'id': LESSONS_PATTERNS['lblRabi']}), 'text', ''
                    )
                    lecure['name'] = getattr(
                        tr.find("a", {'id': LESSONS_PATTERNS['hlName']}), 'text', ''
                    )
                    lecure['serieName'] = getattr(
                        tr.find("a", {'id': LESSONS_PATTERNS['hlSerieName']}), 'text', ''
                    )
                    lecure['date'] = getattr(
                        tr.find("span", {'id': LESSONS_PATTERNS['lblDate']}), 'text', ''
                    )
                    lecure['length'] = getattr(
                        tr.find("span", {'id': LESSONS_PATTERNS['lbllength']}), 'text', ''
                    )
                    link_video = tr.find("a", {'id': LESSONS_PATTERNS['hlVideo']})
                    vid_link = '' if not link_video else link_video.attrs.get('href', '')
                    lecure['videoLink'] = '' if vid_link.endswith('audio/') else vid_link
                    link_audio = tr.find("a", {'id': LESSONS_PATTERNS['hlAudio']})
                    audio_link = '' if not link_audio else link_audio.attrs.get('href', '')
                    lecure['audioLink'] = '' if audio_link.endswith('audio/') else audio_link

                    list_lessons.append(lecure)
            cls.cache_lessons(url, list_lessons)
            return True, list_lessons

    @staticmethod
    def get_link_from_mainpage():
        list_images = []
        resp = requests.get(BASE_BNEI_URL)
        match = re_fetch_bg_image.search(resp.content)
        if match:
            list_images.append(match.group("image"))
        return list_images

    @classmethod
    def init_background_images(cls, join_thread=False):
        def fetch_images():
            for image_link in BACKGROUND_IMAGES_LINKS:
                cls.BACKGROUND_IMAGES.append(requests.get(image_link))

        t = Thread(target=fetch_images)
        t.start()
        if join_thread:
            t.join()

    @classmethod
    def iter_background_images(cls):
        if len(cls.BACKGROUND_IMAGES) < 1:
            image_link = BACKGROUND_IMAGES_LINKS[0]
            firstImage = requests.get(image_link)
            cls.init_background_images()
            yield firstImage
        i = 1
        while True:
            yield cls.BACKGROUND_IMAGES[i % len(cls.BACKGROUND_IMAGES)]
            i += 1

    @classmethod
    def get_cached_lessons(cls, url):
        """
        fetches cached lessons for requested url,
        if has been updated in the last MAX_REFRESH_CACHE
        """
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        req_file_path = parsed_url.path
        hash_cache = hash_dict({"path": req_file_path, **params})
        for root, dirs, fnames in os.walk(CACHE_RESP_DIR):
            for fname in fnames:
                if hash_cache not in fname:
                    continue
                filepath = join(root, fname)
                prev_timestamp = float(".".join(fname.split(".")[:2]))
                now_timestamp = datetime.timestamp(datetime.now())
                if (now_timestamp - prev_timestamp) > MAX_REFRESH_CACHE:
                    os.remove(filepath)
                    return
                new_filepath = join(root, f"{now_timestamp}.{hash_cache}.json")
                os.rename(filepath, new_filepath)
                with open(new_filepath, 'rb') as fh_cache:
                    return json.load(fh_cache)
            return

    @classmethod
    def cache_lessons(cls, url, list_lessons):
        parsed_url = urlparse(url)
        params = params = parse_qs(parsed_url.query)
        req_file_path = parsed_url.path
        hash_cache = hash_dict({"path": req_file_path, **params})
        now_timestamp = datetime.timestamp(datetime.now())
        with open(join(CACHE_RESP_DIR, f"{now_timestamp}.{hash_cache}.json"), 'w', encoding='utf8') as fh_cache:
            json.dump(list_lessons, fh_cache, )
