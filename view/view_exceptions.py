"""
Модуль отвечает за кастомные исключения у view
"""


class InputListWidthException(Exception):
    """
    Класс - исключение. Выбрасывается при некорректном вводе списка ширин (изделий или остатков)

    Args:
        text_width (str) - Введенные данные
        wrong_width (str) - Место, на котором выбросилось исключение
    """
    def __init__(self, text_width: str, wrong_width: str):
        self.__list_width_str: str = text_width
        self.__wrong_width: str = wrong_width

    def __str__(self) -> str:
        return ('Неправильный формат ввода списка ширин. Введенная строка должна представлять'
                'собой числа с плавающей точкой, разделенных пробелом.'
                f'Введенная строка: {self.__list_width_str}\n'
                f'Место выброса ошибки: {self.__wrong_width}')


class NotDigitException(Exception):
    def __init__(self, name: str, wrong_input: str):
        self.__name = name
        self.__wrong_input: str = wrong_input

    def __str__(self) -> str:
        return (f'Параметр {self.__name} должен быть числом!'
                f'Введенное значение: {self.__wrong_input}')
