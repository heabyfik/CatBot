import os.path

from random import randint

phrases = [
    "Конечно, это мой любимый кот Тишка!",
    "Знакомьтесь: Тишка. Разве он не милашка?",
    "Та-дааам. Это Тишка^^",
    "My top cat!",
    "Думаю, самый лучший кот - это мой кот.",
    "Разрешите представить вам моего котика Тишку.",
    "Это Тишка. Вы уже знакомы?)",
    "Самый топовый мурлыка по имени Тишка и мой котофей по совместительству.",
    "Его зовут Тишка. Вы только посмотрите, какой он лапочка!",
]


def get_random_top_cat_photo():
    i = randint(1, 6)
    return open(os.path.dirname(__file__) + f"/../files/cat{i}.jpg", 'rb')


def get_random_top_cat_text():
    i = randint(0, len(phrases) - 1)
    return phrases[i]
