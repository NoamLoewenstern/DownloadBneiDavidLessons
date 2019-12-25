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


def log_called_func(func, func_name="generic func"):
    def dec_func(*args, **kargs):
        print(f"[!] {func_name} Called:\n\targs: {args}\n\tkargs: {kargs}")
        return func(*args, **kargs)
    return dec_func