"""Модуль отвечает за окно с рассчитанной схемой распила"""
from tkinter import Tk, filedialog
from tkinter.ttk import Label, Frame, Button
from typing import Callable

from view.lexicon.lexicon_ru import LABELS, BUTTONS
from business.cut_scheme import CutScheme


def window_with_cut_cheme(cut_scheme: CutScheme, title: str) -> None:
    """
    Функция открывает окно с рассчитанной схемой распила
    :param cut_scheme: Объект схемы распила
    :type cut_scheme: CutScheme
    :param title: Название окна
    :type title: str
    :return: None
    """
    # Создадим новое окно
    window: Tk = Tk()
    window.title(title)
    window.geometry('450x450')

    # Создадим надписи и запишем результаты
    result_text_label: Label = Label(window, text=LABELS['text_result'])
    cut_scheme_label: Label = Label(window, text=cut_scheme.__str__())

    frame_with_waste: Frame = Frame(window)
    total_waste, percent_waste = cut_scheme.waste()

    frame_with_absolute_waste: Frame = Frame(frame_with_waste)
    absolute_waste_text: Label = Label(frame_with_absolute_waste, text=LABELS['total_waste'])
    absolute_waste_result: Label = Label(frame_with_absolute_waste, text=str(total_waste))

    frame_with_percent_waste: Frame = Frame(frame_with_waste)
    percent_waste_text: Label = Label(frame_with_percent_waste, text=LABELS['percent_waste'])
    percent_waste_result: Label = Label(frame_with_percent_waste, text=str(percent_waste))

    save_button: Button = Button(window, text=BUTTONS['save'], command=save_scheme(cut_scheme))

    # Упакуем все объекты
    result_text_label.pack(anchor='nw', padx=5, pady=5)
    cut_scheme_label.pack(anchor='nw', padx=5, pady=5)

    frame_with_waste.pack(anchor='nw')

    frame_with_absolute_waste.pack(anchor='nw')
    frame_with_percent_waste.pack(anchor='nw')

    absolute_waste_text.grid(row=0, column=0, padx=5, pady=5)
    absolute_waste_result.grid(row=0, column=1, padx=5, pady=5)
    percent_waste_text.grid(row=0, column=0, padx=5, pady=5)
    percent_waste_result.grid(row=0, column=1, padx=5, pady=5)

    save_button.pack(anchor='n', padx=5, pady=5)


def save_scheme(cut_scheme: CutScheme) -> Callable:
    """
    Функция сохраняет схему распила в файл
    :param cut_scheme:
    :return:
    """
    def saving_func() -> None:
        filepath = filedialog.asksaveasfilename(defaultextension='txt', initialfile='Схема распила')
        if filepath != "":
            with open(filepath, "w", encoding='utf-8') as file:
                file.write(cut_scheme.__str__())

    return saving_func
