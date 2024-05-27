"""Модуль с исключениями для пакета business"""


class NoRemnantsError(Exception):
    """
    Класс - исключение. Выбрасывается, когда для списка изделий не хватает остатков и цельных профилей
    """
    def __init__(self, title: str, products: list[float], remnants: list[float],
                 current_scheme: dict[tuple[float, int], list[list[float]]]):
        self.__title: str = title
        self.__products: list[float] = products
        self.__remnants: list[float] = remnants
        self.__current_scheme: dict[tuple[float, int], list[list[float]]] = current_scheme

    @property
    def title(self) -> str:
        return self.__title

    @property
    def current_cheme(self) -> dict[tuple[float, int], list[list[float]]]:
        return self.__current_scheme

    @property
    def products(self) -> list[float]:
        return self.__products

    @property
    def remnants(self) -> list[float]:
        return self.__remnants

    def __str__(self) -> str:
        return 'Для данного списка изделий не хватает имеющихся остатков и цельных профилей!\n'

    def __repr__(self) -> str:
        return (f'Для данного списка изделий не хватает имеющихся остатков и цельных профилей!\n'
                f'Список изделий: {self.products}\nСписок остатков: {self.remnants}\n'
                f'Схема распила: {self.current_cheme}')


class WrongSchemeError(NoRemnantsError):
    def __str__(self) -> str:
        return 'Количество распилов больше чем количество имеющихся остатков!'

    def __repr__(self) -> str:
        return (f'Количество распилов больше чем количество имеющихся остатков!'
                f'Список изделий: {self.products}\nСписок остатков: {self.remnants}\n'
                f'Схема распила: {self.current_cheme}')
