"""
Модуль отвечает за кастомные исключения у view
"""
from abc import ABC, abstractmethod


class InputListWidthException(Exception):
    """
    Класс - исключение. Выбрасывается при некорректном вводе списка ширин (изделий или остатков)

    Args:
        text_width (str) - Введенные данные
        wrong_width (str) - Место, в котором выбросилось исключение
        title (str) - Название окна, в котором будет отображаться ошибка
    """
    def __init__(self, text_width: str, wrong_width: str, title: str):
        self.__list_width_str: str = text_width
        self.__wrong_width: str = wrong_width
        self.__title: str = title

    @property
    def title(self) -> str:
        return self.__title

    def __str__(self) -> str:
        return ('Неправильный формат ввода списка ширин. Введенная строка должна представлять '
                'собой числа с плавающей точкой, разделенных пробелом.\n'
                f'Введенная строка: {self.__list_width_str}\n'
                f'Место выброса ошибки: {self.__wrong_width}')


class InputException(Exception, ABC):
    """
    Класс - исключение. От него будут наследоваться исключения ошибки ввода целых и вещественных чисел

    Args:
        title (str) - Название окна, в котором будет отображаться ошибка
        wrong_input (str) - Неправильный ввод
    """
    def __init__(self, title: str, wrong_input: str) -> None:
        self.__title: str = title
        self.__wrong_input: str = wrong_input

    @property
    def title(self) -> str:
        return self.__title

    @property
    def wrong_input(self) -> str:
        return self.__wrong_input

    @abstractmethod
    def __str__(self) -> str:
        pass


class InputFloatExc(InputException):
    def __str__(self) -> str:
        return (f'Параметр: "{self.title}" должен быть вещественным числом (числом с плавающей запятой)!\n'
                f'Введенное значение: {self.wrong_input}')


class InputIntExc(InputException):
    def __str__(self) -> str:
        return (f'Параметр: "{self.title}" должен быть целым числом!\n'
                f'Введенное значение: {self.wrong_input}')
