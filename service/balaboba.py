import json
import urllib.request

from random import randint

seeds = [
    "Кот",
    "Котик",
    "Котечка",
    "Котейка",
    "Котенок",
    "Кошка",
    "Кошечка",
    "Киса",
    "Котяра",
    "Кисонька",
    "Котята",
    "Кошки",
    "Коты",
    "Котики",
    "Кошачьи",
    "Котофей",
    "Усатый-полосатый",
    "Мурлыка",
    "Котяра",
    "Васька"
]


def get_random_story(intro=0):
    i = randint(0, len(seeds) - 1)
    seed = seeds[i]

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 '
                      '(KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Origin': 'https://yandex.ru',
        'Referer': 'https://yandex.ru/',
    }

    API_URL = 'https://zeapi.yandex.net/lab/api/yalm/text3'
    payload = {"query": seed, "intro": intro, "filter": 1}
    params = json.dumps(payload).encode('utf-8')

    try:
        req = urllib.request.Request(API_URL, data=params, headers=headers)
        response = urllib.request.urlopen(req)
        j = json.loads(response.read().decode('utf-8'))

        return j["query"] + j["text"]
    except Exception as e:
        print(e)
        return "Ой, что-то пошло не так. Повторите попытку позже."
