"""
Модуль отвечает за работу главного окна
"""
from tkinter.ttk import Notebook, Frame
from tkinter import Tk
import tkinter as tk
from tkinter import *
from tkinter import ttk

from frames.simple_cutting_calc import SimpleCutCalc
from lexicon.lexicon_ru import FRAMES


def main():
    root = Tk()
    root.title("Калькулятор профилей (демо - v1.0.0)")
    root.geometry("450x450")

    notebook: Notebook = Notebook()
    notebook.pack(expand=True, fill=tk.BOTH)

    frame1: Frame = SimpleCutCalc(notebook).get_frame()
    frame1.pack(fill=tk.BOTH, expand=True)

    notebook.add(frame1, text=FRAMES['simple_cut'])

    root.mainloop()

    root.mainloop()


if __name__ == "__main__":
    main()
