import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Label, Frame
from tkinter import Toplevel
from typing import Optional


class Tooltip:
    """
    Класс, отвечающий за показ всплывающих подсказок

    Args:
        label (Label) - Объект Label, при наведении курсора на которого показывается всплывающее окно
        text (str) - Текст всплывающей подсказки
    """
    def __init__(self, label: Label, text: str):
        self.__label: Label = label
        self.__text: str = text
        self.__tooltip: Optional[Toplevel] = None
        self.__label.bind("<Enter>", self.__show)
        self.__label.bind("<Leave>", self.__hide)

    def __show(self, event=None):
        x, y, _, _ = self.__label.bbox()
        x += self.__label.winfo_rootx() + 25
        y += self.__label.winfo_rooty() + 25

        self.__tooltip = Toplevel(self.__label)
        self.__tooltip.wm_overrideredirect(True)
        self.__tooltip.wm_geometry(f"+{x}+{y}")

        tooltip_text: Label = Label(self.__tooltip, text=self.__text,
                                    background="#ffffe0", relief="solid", borderwidth=1)
        tooltip_text.pack()

    def __hide(self, event=None):
        if self.__tooltip:
            self.__tooltip.destroy()
            self.__tooltip = None


def get_help_tooltip(root: Frame, tooltip_text: str, label_text: str = '(?)') -> Label:
    """
    Функция создает объект Label с всплывающей подсказкой
    :param root: Корневой фрейм, к которому привязывается подсказка.
    :type root: Frame
    :param tooltip_text: текст всплывающей подсказки
    :type tooltip_text: str
    :param label_text: Текст объекта Label, при наведении курсора на которой появляется всплывающая подсказка
    :type label_text: str
    :return: Объект Label с всплывающей подсказкой
    :rtype: Label
    """
    tooltip_label: Label = Label(root, text=label_text)
    tooltip: Tooltip = Tooltip(tooltip_label, tooltip_text)

    return tooltip_label


if __name__ == '__main__':
    # Create the main window
    window = tk.Tk()
    window.title("PythonExamples.org")
    window.geometry("300x200")

    # Create a label with tooltip
    label = ttk.Label(window, text="Hello World! Hover me.")
    label.pack()

    # Create a tooltip for the label
    test_tooltip = Tooltip(label, "This is a tooltip")

    # Run the application
    window.mainloop()
