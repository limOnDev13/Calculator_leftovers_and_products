"""
Модуль отвечает за вкладку обычного калькулятора распила профилей
"""
from tkinter.ttk import Notebook, Frame, Label, Entry, Button
from tkinter.scrolledtext import ScrolledText
from tkinter import StringVar
import tkinter.messagebox as msg_box

from view.lexicon.lexicon_ru import LABELS, BUTTONS
from view.view_exceptions import InputListWidthException


class SimpleCutCalc:
    """
    Класс отвечает за фрейм с простым калькулятором распила

    Args:
        notebook (Notebook) - Объект списка закладок
    """
    def __init__(self, notebook: Notebook):
        self.__notebook: Notebook = notebook
        self.__frame: Frame = Frame(notebook)
        self.__products: StringVar = StringVar()
        self.__remnants: StringVar = StringVar()
        self.__correction: StringVar = StringVar()
        self.__min_remnant: StringVar = StringVar()
        self.__whole_profile_len: StringVar = StringVar()
        self.__number_whole_profiles: StringVar = StringVar()
        self.__cutting_width: StringVar = StringVar()

    def get_data(self, input_products: ScrolledText, input_remnants: ScrolledText,
                 ) -> None:
        """
        Метод считывает введенные ширины изделий и остатков при нажатии кнопки расчет
        :return: None
        """
        products_str: str = input_products.get('1.0', 'end-1c')  # По этим индексам будет считан весь текст
        remnants_str: str = input_remnants.get('1.0', 'end-1c')

        self.__products

    def get_frame(self) -> Frame:
        # Разделим все на разные фреймы для красоты
        input_products_and_remnants_frame: Frame = Frame(self.__frame)
        # 1) Ввод ширин изделий из наряда
        input_products_label: Label = Label(input_products_and_remnants_frame, text=LABELS['input_products'])
        input_products_label.pack(anchor='nw', padx=5, pady=5)

        input_products_text: ScrolledText = ScrolledText(
            input_products_and_remnants_frame, width=50, height=5)

        input_products_text.pack(anchor='nw', padx=5, pady=5)

        # 2) Ввод остатков
        input_remnants_label: Label = Label(input_products_and_remnants_frame, text=LABELS['input_remnants'])
        input_remnants_label.pack(anchor='nw', padx=5, pady=5)

        input_remnants_text: ScrolledText = ScrolledText(
            input_products_and_remnants_frame, width=50, height=5)
        input_remnants_text.pack(anchor='nw', padx=5, pady=5)
        # Упакуем полученный фрейм
        input_products_and_remnants_frame.pack(anchor='nw')

        # 3) Ввод основных параметров
        grid_data: list[tuple[str, StringVar]] = [
            (LABELS['input_correction'], self.__correction),
            (LABELS['input_min_remnant'], self.__min_remnant),
            (LABELS['input_whole_profile'], self.__whole_profile_len),
            (LABELS['input_number_profiles'], self.__number_whole_profiles),
            (LABELS['input_cutting_width'], self.__cutting_width)
        ]

        for num, data in enumerate(grid_data):
            # Сделаем для каждого ввода отдельный фрейм и упакуем все вводы с помощью grid
            # Так, текст и ввод будут красиво расположены
            frame: Frame = Frame(self.__frame)
            label: Label = Label(frame, text=data[0])
            entry: Entry = Entry(frame, width=10, textvariable=data[1])

            label.grid(row=num, column=0, padx=5, pady=5)
            entry.grid(row=num, column=1, padx=5, pady=5)

            # Упакуем фрейм
            frame.pack(anchor='nw')

        # 4) Добавим кнопки для расчета и и сброса введенных данных
        frame_with_buttons: Frame = Frame(self.__frame)

        # 5) Добавим отслеживание переменных
        self.__products.trace_add('read', self.__check_products)
        self.__remnants.trace_add('read', self.__check_remnants)
        self.__products.trace_add('read', self.__check_products)
        self.__products.trace_add('read', self.__check_products)
        self.__products.trace_add('read', self.__check_products)

        buttons: list[Button] = [
            Button(frame_with_buttons, text=BUTTONS['quick_calc']),
            Button(frame_with_buttons, text=BUTTONS['middle_calc']),
            Button(frame_with_buttons, text=BUTTONS['reset']),
        ]
        for num, button in enumerate(buttons):
            button.grid(row=0, column=num)

        frame_with_buttons.pack(anchor='ne')

        return self.__frame

    @classmethod
    def __check_format_list_width(cls, profiles_str: str) -> None:
        """
        Метод проверяет корректность ввода ширин нескольких изделий или остатков.
        Введенная строка должна представлять собой числа с плавающей точкой, разделенные пробелами
        :param profiles_str: Введенная строка
        :type profiles_str: str
        :return: None
        """
        numbers_str: list[str] = profiles_str.split()

        for number in numbers_str:
            if not number.isdigit():
                raise InputListWidthException(profiles_str, number)

    def __check_products(self, *args) -> None:
        """
        Метод проверяет корректность ввода списка ширин изделий
        :param args:
        :return: None
        """
        products_str = self.__products.get()

        try:
            self.__check_format_list_width(products_str)
        except InputListWidthException as exc:
            msg_box.showerror(
                title='Ошибка ввода списка изделий',
                message=exc.__str__()
            )

    def __check_remnants(self, *args) -> None:
        """
        Метод проверяет корректность ввода списка остатков
        :param args:
        :return: None
        """
        remnants_str = self.__remnants.get()

        try:
            self.__check_format_list_width(remnants_str)
        except InputListWidthException as exc:
            msg_box.showerror(
                title='Ошибка ввода списка остатков',
                message=exc.__str__()
            )

    def __check_digit(self, *args):
        pass
