import re
import requests
from flask import jsonify
from bs4 import BeautifulSoup


LESSONS_PATTERNS = {
    'lblSubject': re.compile('.*_lblSubject'),
    'lblRabi': re.compile('.*_lblRabi'),
    'hlName': re.compile('.*hlName'),
    'hlSerieName': re.compile('.*_hlSerieName'),
    'lblDate': re.compile('.*_lblDate'),
    'lbllength': re.compile('.*_lbllength'),
    'hlVideo': re.compile('.*_hlVideo'),
    'hlAudio': re.compile('.*_hlAudio'),

}


def get_list_lessons(url):
    try:
        response = requests.get(url)
    except:
        return False, jsonify(status="Error", url=url, msg="Error. Invalid URL")
    if not response.ok:
        return False, jsonify(status="Error", url=url, msg="Error. Invalid URL")
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
            tr.find("span", {"id": LESSONS_PATTERNS['lblSubject']}), 'text', '')
        lecure['rabi'] = getattr(
            tr.find("span", {"id": LESSONS_PATTERNS['lblRabi']}), 'text', '')
        lecure['name'] = getattr(
            tr.find("a", {"id": LESSONS_PATTERNS['hlName']}), 'text', '')
        lecure['serieName'] = getattr(
            tr.find("a", {"id": LESSONS_PATTERNS['hlSerieName']}), 'text', '')
        lecure['date'] = getattr(
            tr.find("span", {"id": LESSONS_PATTERNS['lblDate']}), 'text', '')
        lecure['length'] = getattr(
            tr.find("span", {"id": LESSONS_PATTERNS['lbllength']}), 'text', '')
        link_video = tr.find("a", {"id": LESSONS_PATTERNS['hlVideo']})
        lecure['videoLink'] = '' if not link_video else link_video.attrs['href']
        link_audio = tr.find("a", {"id": LESSONS_PATTERNS['hlAudio']})
        lecure['audioLink'] = '' if not link_audio else link_audio.attrs['href']

        list_lectures.append(lecure)

    return True, list_lectures
