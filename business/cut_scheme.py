"""Модуль отвечает за обработку схемы распила"""
from business.business_exceptions import WrongSchemeError


class CutScheme:
    """
    Класс для обработки схемы распила

    Args:
        cut_scheme (dict[tuple[float, int], list[list[float]]]) - Схема распила
        min_remnant (float) - Минимальная длина остатка
        cut_width (float) - Поправка к ширине изделия
    """
    def __init__(self, cut_scheme: dict[tuple[float, int], list[list[float]]],
                 min_remnant: float, cut_width: float) -> None:
        self.__cut_scheme: dict[tuple[float, int], list[list[float]]] = cut_scheme
        self.__min_remnant: float = min_remnant
        self.__cut_width: float = cut_width

    @property
    def cut_scheme(self) -> dict[tuple[float, int], list[list[float]]]:
        """Геттер для self.__cut_scheme"""
        return self.__cut_scheme

    def __str__(self) -> str:
        """
        Функция преобразует схему распила в удобно читаемый текст
        :return: Строковое представление распила
        :rtype: str
        """
        result_string: str = ''

        for remnant, opt_products in self.__cut_scheme.items():
            result_string += f'{remnant}:\n'
            for opt_product in opt_products:
                result_string += (f'\t{opt_product} = {round(sum(opt_product), 3)} '
                                  f'({remnant[0]}, ост: {round(remnant[0] - sum(opt_product), 3)})\n')

        return result_string

    def restore_order(self) -> None:
        """
        В ключах в схеме распила указываются количества имеющихся одинаковых остатков,
        но при этом не все они могут использоваться. Данный метод правит ключи в распиле так, чтобы количество
        распилов было равно количеству остатков в ключе
        :raise WrongSchemeError: если количество одинаковых остатков меньше чем количество распилов для данной длинны
        остатка
        :return: None
        """
        remnants: set[tuple[float, int]] = set(self.__cut_scheme.keys())

        for remnant in remnants:
            # Если добавился пустой распил - удалим его
            if len(self.__cut_scheme[remnant]) == 0:
                self.__cut_scheme.pop(remnant)
            elif remnant[1] > len(self.__cut_scheme[remnant]):
                new_key: tuple[float, int] = (remnant[0], len(self.__cut_scheme[remnant]))
                self.__cut_scheme[new_key] = self.__cut_scheme.pop(remnant)
            elif remnant[1] < len(self.__cut_scheme[remnant]):
                raise WrongSchemeError(title='Неправильный расчет распила', current_scheme=self.__cut_scheme)

    def waste(self) -> tuple[float, float]:
        """
        Метод производит расчет отхода в данной схеме распила
        :return: Абсолютный и относительный отходы
        :rtype: tuple[float, float]
        """
        total_waste: float = 0.0
        total_remnant: float = 0.0

        for remnant, cuttings in self.__cut_scheme.items():
            total_remnant += remnant[0] * remnant[1]

            for cut in cuttings:
                total_waste += self.__cut_width * len(cut)  # Учет стружки
                waste: float = remnant[0] - sum(cut) - self.__cut_width * len(cut)
                # Если остаток меньше, чем минимальная длина остатка - в отход
                if waste < self.__min_remnant:
                    total_waste += waste

        waste_percent: float = round((total_waste * 100 / total_remnant), 3)

        return total_waste, waste_percent
