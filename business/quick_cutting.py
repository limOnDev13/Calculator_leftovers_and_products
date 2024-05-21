"""Модуль, отвечающий за работу алгоритма QuickCutting"""
from copy import deepcopy
from typing import Optional

from business.cutting import Cutting
from business.business_exceptions import NoRemnantsError


class QuickCutting(Cutting):
    __name__ = 'QuickCutting'

    def __str__(self) -> str:
        return ('Данный метод сначала ищет наименьший остаток, считает для него оптимальный распил,'
                ' и так по очереди рассчитывает распил для всех изделий')

    def cut(self) -> dict[tuple[float, int], list[list[float]]]:
        """
        Метод для расчета распила. Данный метод сначала ищет наименьший остаток, считает для него оптимальный распил,
        и так по очереди рассчитывает распил для всех изделий
        :return: Распил. Имеет тип словаря, ключи - кортежи, где первый элемент - длина остатка,
        второй - количество остатков данной длины. Значения словаря - список списков изделий для одного такого остатка
        :rtype: dict[tuple[float, int], list[list[float]]]
        """
        cutting_scheme: dict[tuple[float, int], list[list[float]]] = dict()
        current_remnants: set[tuple[float, int]] = self.generate_keys(self.remnants, min(self.products))
        current_products: list[float] = deepcopy(self.products)
        number_used_profiles: int = 0

        while current_products:
            min_remnant: Optional[tuple[float, int]] = None

            # Если остатков нет, но есть цельные профили, то будем использовать их
            if not current_remnants and number_used_profiles < self.number_whole_profiles:
                number_used_profiles += 1
            # Если нет остатков и нет цельных профилей, то выбросим исключение
            elif not current_remnants and number_used_profiles == self.number_whole_profiles:
                raise NoRemnantsError(title='Не хватает остатков и цельных профилей', current_scheme=cutting_scheme)
            # Если остатки имеются, то возьмем наименьший
            else:
                min_remnant: tuple[float, int] = min(current_remnants, key=lambda remnant: remnant[0])

            # Рассчитаем для него оптимальный распил
            current_cutting: Optional[list[float]] = None
            if min_remnant is None:
                current_cutting = self.calculate_min_waste(self.whole_profile_length, current_products)
            else:
                current_cutting = self.calculate_min_waste(min_remnant[0], current_products)

            # Удалим полученные изделия
            current_products = self.remove_list_from_array(current_products, current_cutting)

            # Если мы брали цельный профиль (min_remnant = None), то добавим ключ в словарь
            # Для этого удалим значение по старому ключу и добавим его по новому
            # - в нем количество цельных профилей на 1 больше
            if min_remnant is None:
                if (self.whole_profile_length, number_used_profiles - 1) in cutting_scheme:
                    cutting_scheme[(self.whole_profile_length, number_used_profiles)] = (
                        cutting_scheme.pop((self.whole_profile_length, number_used_profiles - 1)))
                    cutting_scheme[(self.whole_profile_length, number_used_profiles)].append(current_cutting)
                else:
                    cutting_scheme[(self.whole_profile_length, number_used_profiles)] = [current_cutting]

            # Если использовали остаток, то добавим его
            else:
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

        return cutting_scheme
