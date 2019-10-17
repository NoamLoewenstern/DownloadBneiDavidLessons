import requests
import re
from threading import Thread
from config import BASE_BNEI_URL, BACKGROUND_IMAGES_LINKS
from json import loads
global BACKGROUND_IMAGES
BACKGROUND_IMAGES = []

re_fetch_bg_image = re.compile('background:url\((?P<image>.+?)\)')


def get_link_from_mainpage():
    list_images = []
    resp = requests.get(BASE_BNEI_URL)
    match = re_fetch_bg_image.search(resp.content)
    if match:
        list_images.append(match.group('image'))
    return list_images


def init_background_images(join_thread=False):
    def fetch_images():
        global BACKGROUND_IMAGES
        BACKGROUND_IMAGES = []
        for image_link in BACKGROUND_IMAGES_LINKS:
            BACKGROUND_IMAGES.append(requests.get(image_link))
    t = Thread(target=fetch_images)
    t.start()
    if join_thread:
        t.join()


def iter_background_images():
    global BACKGROUND_IMAGES
    if len(BACKGROUND_IMAGES) < 1:
        image_link = BACKGROUND_IMAGES_LINKS[0]
        firstImage = requests.get(image_link)
        init_background_images()
        yield firstImage
    i = 1
    while True:
        yield BACKGROUND_IMAGES[i % len(BACKGROUND_IMAGES)]
        i += 1


def jsonified(data):
    try:
        return loads(data)
    except:
        return ''
