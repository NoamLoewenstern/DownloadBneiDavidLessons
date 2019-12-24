from json import loads, dumps
import hashlib


def jsonified(data):
    try:
        return loads(data)
    except ValueError:
        return ""

def hash_dict(dct):
    md5 = hashlib.md5()
    md5.update(dumps(dct, sort_keys=True).encode('utf8'))
    return md5.hexdigest()