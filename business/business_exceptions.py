"""Модуль с исключениями для пакета business"""


class NoRemnantsError(Exception):
    """
    Класс - исключение. Выбрасывается, когда для списка изделий не хватает остатков и цельных профилей
    """
    def __init__(self, title: str, current_scheme: dict[tuple[float, int], list[list[float]]]):
        self.__title: str = title
        self.__current_scheme: dict[tuple[float, int], list[list[float]]] = current_scheme

    @property
    def title(self) -> str:
        return self.__title

    @property
    def current_cheme(self) -> dict[tuple[float, int], list[list[float]]]:
        return self.__current_scheme

    def __str__(self) -> str:
        return 'Для данного списка изделий не хватает имеющихся остатков и цельных профилей!'


class WrongSchemeError(NoRemnantsError):
    def __str__(self) -> str:
        return f'Количество распилов больше чем количество имеющихся остатков!\nРаспил: {self.current_cheme}'
