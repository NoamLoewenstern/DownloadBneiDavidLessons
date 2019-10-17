BASE_BNEI_URL = 'http://www.bneidavid.org'
list_background_paths = ['/Items/05889/001.jpg',
                         '/Items/05890/002.jpg',
                         '/Items/05891/003.jpg',
                         '/Items/00427/004.jpg',
                         '/Items/00426/005.jpg',
                         '/Items/00428/006.jpg',
                         '/Items/00429/007.jpg']


BACKGROUND_IMAGES_LINKS = [BASE_BNEI_URL +
                           bg_pic for bg_pic in list_background_paths]

DEFAULT_LESSONS_PAGE = BASE_BNEI_URL + \
    '/Web/He/VirtualTorah/Lessons/Default.aspx'

DBG = False
