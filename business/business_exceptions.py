"""Модуль с исключениями для пакета business"""
from business.cut_scheme import CutScheme


class NoRemnantsError(Exception):
    """
    Класс - исключение. Выбрасывается, когда для списка изделий не хватает остатков и цельных профилей
    """
    def __init__(self, title: str, cut_scheme: CutScheme):
        self.__title: str = title
        self.__cut_scheme: CutScheme = cut_scheme

    @property
    def title(self) -> str:
        return self.__title

    @property
    def cut_scheme(self) -> CutScheme:
        return self.__cut_scheme

    def __str__(self) -> str:
        return 'Для данного списка изделий не хватает имеющихся остатков и цельных профилей!\n'

    def __repr__(self) -> str:
        return (f'Для данного списка изделий не хватает имеющихся остатков и цельных профилей!\n'
                f'Список изделий: {self.cut_scheme.products}\nСписок остатков: {self.cut_scheme.remnants}\n'
                f'Схема распила:\n{self.cut_scheme.__str__()}')
