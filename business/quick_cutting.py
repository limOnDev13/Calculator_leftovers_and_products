"""Модуль, отвечающий за работу алгоритма QuickCutting"""
from copy import deepcopy

from business.cutting import Cutting
from business.business_exceptions import NoRemnantsError
from business.cut_scheme import CutScheme


class QuickCutting(Cutting):
    __name__ = 'QuickCutting'

    def __str__(self) -> str:
        return ('Данный метод сначала ищет наименьший остаток, считает для него оптимальный распил,'
                ' и так по очереди рассчитывает распил для всех изделий')

    def cut(self) -> CutScheme:
        """
        Метод для расчета распила. Данный метод сначала ищет наименьший остаток, считает для него оптимальный распил,
        и так по очереди рассчитывает распил для всех изделий
        :return: Распил. Имеет тип словаря, ключи - кортежи, где первый элемент - длина остатка,
        второй - количество остатков данной длины. Значения словаря - список списков изделий для одного такого остатка
        :rtype: dict[tuple[float, int], list[list[float]]]
        """
        cutting_scheme: dict[tuple[float, int], list[list[float]]] = dict()
        current_remnants: set[tuple[float, int]] = self.generate_keys(self.remnants, min(self.products))
        # Добавим цельные профили в список остатков
        current_remnants.add((self.whole_profile_length, self.number_whole_profiles))
        current_products: list[float] = deepcopy(self.products)

        while current_products:
            # Если нет остатков и нет цельных профилей, то выбросим исключение
            if not current_remnants:
                beautiful_scheme: CutScheme = CutScheme(
                    cut_scheme=cutting_scheme, min_remnant=self.min_rest_length, cut_width=self.cutting_width,
                    products=self.products, remnants=self.remnants)
                beautiful_scheme.restore_order()
                raise NoRemnantsError(title='Не хватает остатков и цельных профилей', cut_scheme=beautiful_scheme)

            # Если остатки имеются, то возьмем наименьший
            min_remnant: tuple[float, int] = min(current_remnants, key=lambda remnant: remnant[0])

            # Рассчитаем для него оптимальный распил
            if min_remnant is None:
                current_cutting: list[float] = self.calculate_min_waste(self.whole_profile_length, current_products)
            else:
                current_cutting: list[float] = self.calculate_min_waste(min_remnant[0], current_products)

            # Удалим полученные изделия
            current_products = self.remove_list_from_array(current_products, current_cutting)

            # Удалим использованные остатки
            if min_remnant in cutting_scheme:
                cutting_scheme[min_remnant].append(current_cutting)
            else:
                cutting_scheme[min_remnant] = [current_cutting]

            # Уберем использованный остаток и полученные изделия для следующих итераций
            if len(cutting_scheme[min_remnant]) == min_remnant[1]:
                current_remnants.remove(min_remnant)

            # После распила могли остаться остатки, которые меньше всех оставшихся изделий - уберем их
            if len(current_products) >= 1:
                current_remnants = {remnant for remnant in current_remnants if remnant[0] >= min(current_products)}

        # В схеме распила количество остатков в ключе может быть больше количества распилов для данного остатка -
        # исправим это
        beautiful_scheme: CutScheme = CutScheme(
            cut_scheme=cutting_scheme, min_remnant=self.min_rest_length, cut_width=self.cutting_width,
            products=self.products, remnants=self.remnants)
        beautiful_scheme.restore_order()
        return beautiful_scheme
