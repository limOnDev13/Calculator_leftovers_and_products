"""
Модуль отвечает за вкладку обычного калькулятора распила профилей
"""
from tkinter.ttk import Notebook, Frame, Label, Entry, Button
from tkinter.scrolledtext import ScrolledText
from tkinter import StringVar
import tkinter.messagebox as msg_box
from typing import Optional, Callable, Type
import re
from re import Match
from loguru import logger

from view.lexicon.lexicon_ru import LABELS, BUTTONS, ERROR_LABELS, TOOLTIPS
from view.view_exceptions import InputListWidthException, InputIntExc, InputFloatExc
from view.frames.result_cut_window import window_with_cut_cheme
from view.frames.tooltips import get_help_tooltip
from business.cutting import Cutting
from business.quick_cutting import QuickCutting
from business.middle_cutting import MiddleCutting
from business.cut_scheme import CutScheme, WrongSchemeError
from business.business_exceptions import NoRemnantsError


class SimpleCutCalc:
    """
    Класс отвечает за фрейм с простым калькулятором распила

    Args:
        notebook (Notebook) - Объект списка закладок
    """
    def __init__(self, notebook: Notebook):
        self.__notebook: Notebook = notebook
        self.__frame: Frame = Frame(notebook)
        self.__input_products_text: Optional[ScrolledText] = None
        self.__input_remnants_text: Optional[ScrolledText] = None
        self.__correction: StringVar = StringVar()
        self.__min_remnant: StringVar = StringVar()
        self.__whole_profile_len: StringVar = StringVar()
        self.__number_whole_profiles: StringVar = StringVar()
        self.__cutting_width: StringVar = StringVar()

    def get_frame(self) -> Frame:
        # 1) Ввод ширин изделий из наряда
        products_frame: Frame = Frame(self.__frame)
        input_products_label: Label = Label(products_frame, text=LABELS['input_products'])
        help_products: Label = get_help_tooltip(products_frame, tooltip_text=TOOLTIPS['input_products'])

        self.__input_products_text = ScrolledText(
            self.__frame, width=50, height=5)

        # 2) Ввод остатков
        remnants_frame: Frame = Frame(self.__frame)
        input_remnants_label: Label = Label(remnants_frame, text=LABELS['input_remnants'])
        help_remnants: Label = get_help_tooltip(remnants_frame, tooltip_text=TOOLTIPS['input_remnants'])

        self.__input_remnants_text = ScrolledText(
            self.__frame, width=50, height=5)

        # 3) Добавим кнопки для расчета и и сброса введенных данных
        frame_with_buttons: Frame = Frame(self.__frame)

        buttons: list[Button] = [
            Button(frame_with_buttons, text=BUTTONS['quick_calc'], command=self.__calc_cut(QuickCutting)),
            Button(frame_with_buttons, text=BUTTONS['middle_calc'], command=self.__calc_cut(MiddleCutting)),
            Button(frame_with_buttons, text=BUTTONS['reset'], command=self.__reset_button),
        ]

        # 4) Упакуем ввод изделий
        products_frame.pack(anchor='nw', padx=5, pady=5)
        input_products_label.grid(row=0, column=0, padx=5, pady=5)
        help_products.grid(row=0, column=1, padx=1, pady=5)
        self.__input_products_text.pack(anchor='nw', padx=5, pady=5)
        # Упакуем ввод остатков
        remnants_frame.pack(anchor='nw', padx=5, pady=5)
        input_remnants_label.grid(row=0, column=0, padx=5, pady=5)
        help_remnants.grid(row=0, column=1, padx=1, pady=5)
        self.__input_remnants_text.pack(anchor='nw', padx=5, pady=5)

        # 5) Ввод основных параметров
        grid_data: list[tuple[str, StringVar]] = [
            ('input_correction', self.__correction),
            ('input_min_remnant', self.__min_remnant),
            ('input_whole_profile', self.__whole_profile_len),
            ('input_number_profiles', self.__number_whole_profiles),
            ('input_cutting_width', self.__cutting_width)
        ]

        for num, data in enumerate(grid_data):
            # Сделаем для каждого ввода отдельный фрейм и упакуем все вводы с помощью grid
            # Так, текст и ввод будут красиво расположены
            frame: Frame = Frame(self.__frame)
            label: Label = Label(frame, text=LABELS[data[0]])
            entry: Entry = Entry(frame, width=10, textvariable=data[1])
            help_label: Label = get_help_tooltip(frame, TOOLTIPS[data[0]])

            label.grid(row=0, column=0, padx=5, pady=5)
            entry.grid(row=0, column=1, padx=5, pady=5)
            help_label.grid(row=0, column=2, padx=1, pady=5)

            # Упакуем фрейм
            frame.pack(anchor='nw')

        # Упакуем кнопки
        for num, button in enumerate(buttons):
            button.grid(row=0, column=num)
        frame_with_buttons.pack(anchor='se')

        return self.__frame

    @classmethod
    def __check_format_list_width(cls, profiles: ScrolledText, title_error: str) -> list[float]:
        """
        Метод проверяет корректность ввода ширин нескольких изделий или остатков.
        Введенная строка должна представлять собой числа с плавающей точкой, разделенные пробелами
        :param profiles: Объект окна, в которое вводили список ширин
        :type profiles: ScrolledText
        :param title_error: Название окна, в котором будет отображаться ошибка
        :type title_error: str
        :raise InputListWidthException: Если ввод пустой или не корректен
        :return: Список введенных ширин
        :rtype: list[float]
        """
        profiles_str: str = profiles.get('1.0', 'end-1c')  # По этим индексам будет считан весь текст
        numbers_str: list[str] = profiles_str.split()

        for number in numbers_str:
            match: Optional[Match[str]] = re.search(r'\d+\.?\d*', number)

            # Если хотя бы одно слово не является числом - выбрасываем ошибку
            if not match or match.end() != len(number):
                raise InputListWidthException(profiles_str, number, title_error)

        return [float(profile) for profile in numbers_str]

    @classmethod
    def __check_param(cls, param: StringVar, param_name: str) -> float:
        """
        Метод для проверки введенного параметра, который должен быть вещественным числом
        :param param: Введенный параметр
        :type param: StringVar
        :param param_name: Название параметра (необходимо для красивой печати)
        :type param_name: str
        :raise InputFloatExc: Если введенное значение не является вещественным числом
        :return: Введенное float значение
        :rtype: float
        """
        param_str: str = param.get()
        match: Optional[Match[str]] = re.search(r'\d+\.?\d*', param_str)

        if not match or match.end() != len(param_str):
            raise InputFloatExc(
                title=param_name,
                wrong_input=param_str)

        return float(param_str)

    def __check_number_whole_profiles(self) -> int:
        """
        Метод для проверки корректности введенного количества целых профилей
        :raise InputIntExc: Если введенное значение не является вещественным числом
        :return: Введенное количество целых профилей
        :rtype: int
        """
        numer_whole_profiles: str = self.__number_whole_profiles.get()

        if not numer_whole_profiles.isdigit():
            raise InputIntExc(
                title=ERROR_LABELS['number_whole_profiles'],
                wrong_input=numer_whole_profiles)

        return int(numer_whole_profiles)

    def __calc_cut(self, algorithm: Type[Cutting]) -> Callable:
        """
        Метод срабатывает при нажатии на кнопку Расчет распила. Он проверяет корректность введенных значений,
        если нет ошибок - производит расчет с помощью выбранного алгоритма.
        Пока он будет выводить результат в терминал
        :return: None
        """
        def __calc_cut_with_algorithm() -> None:
            # Проверим введенные данные
            try:
                products: list[float] = self.__check_format_list_width(
                    self.__input_products_text, ERROR_LABELS['products'])
                remnants: list[float] = self.__check_format_list_width(
                    self.__input_remnants_text, ERROR_LABELS['remnants'])
                corr: float = self.__check_param(self.__correction, ERROR_LABELS['correction'])

                if products is not None and remnants is not None:
                    algorithm_cut: Cutting = algorithm(
                        remnants=remnants,
                        in_products=products,
                        correction=corr,
                        min_rest_length=self.__check_param(self.__min_remnant, ERROR_LABELS['min_remnant']),
                        whole_profile_length=self.__check_param(
                            self.__whole_profile_len, ERROR_LABELS['whole_profile']),
                        number_whole_profiles=self.__check_number_whole_profiles(),
                        cutting_width=self.__check_param(self.__cutting_width, ERROR_LABELS['cut_width'])
                    )
                    logger.success('Данные введены верно!')
                    # Распечатаем схему распила
                    cut_scheme: CutScheme = algorithm_cut.cut()
                    logger.success('Схема распила рассчитана верно!')
                    window_with_cut_cheme(cut_scheme, title=f'Схема распила: {algorithm.__name__}')

            except (InputFloatExc, InputIntExc) as exc:
                logger.warning(exc.__str__())

                msg_box.showerror(
                    title=ERROR_LABELS['error_input'] + exc.title,
                    message=exc.__str__()
                )
            except InputListWidthException as exc:
                logger.warning(exc.__str__())

                msg_box.showerror(
                    title=exc.title,
                    message=exc.__str__()
                )
            except WrongSchemeError as exc:
                logger.exception(exc.__repr__())
            except NoRemnantsError as exc:
                logger.warning(exc.__repr__())

                msg_box.showerror(
                    title=exc.title,
                    message=exc.__str__()
                )

                window_with_cut_cheme(exc.cut_scheme, title=f'Схема распила: {algorithm.__name__}')

        return __calc_cut_with_algorithm

    def __reset_button(self) -> None:
        if self.__input_products_text is not None:
            self.__input_products_text.delete('1.0', 'end-1c')
        if self.__input_remnants_text is not None:
            self.__input_remnants_text.delete('1.0', 'end-1c')
        self.__correction.set('')
        self.__min_remnant.set('')
        self.__whole_profile_len.set('')
        self.__number_whole_profiles.set('')
        self.__cutting_width.set('')


if __name__ == '__main__':
    pass
