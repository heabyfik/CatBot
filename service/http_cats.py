import requests


valid_status_codes = [
    100, 101, 102,
    200, 201, 202,
    203, 204, 206,
    207, 300, 301,
    302, 303, 304,
    305, 307, 308,
    400, 401, 402,
    403, 404, 405,
    406, 407, 408,
    409, 410, 411,
    412, 413, 414,
    415, 416, 417,
    418, 420, 421,
    422, 423, 424,
    425, 426, 429,
    431, 444, 450,
    451, 497, 498,
    499, 500, 501,
    502, 503, 504,
    506, 507, 508,
    509, 510, 511,
    521, 523, 525,
    599,
]


def is_valid_status_code(status_code: int) -> bool:
    if int(status_code) in valid_status_codes:
        return True

    return False


def get_http_cat(status_code) -> bytes:
    r = requests.get(f'https://http.cat/{status_code}')
    if r.status_code == 200:
        return r.content
    else:
        return bytes()
