from business.cutting import Cutting
from copy import deepcopy


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

        while current_products and current_remnants:
            # Найдем наименьший остаток
            min_remnant: tuple[float, int] = min(current_remnants, key=lambda remnant: remnant[0])

            # Рассчитаем для него оптимальный распил
            current_cutting: list[float] = self.calculate_min_waste(min_remnant[0], current_products)

            # Добавим распил в словарь
            if min_remnant in cutting_scheme:
                cutting_scheme[min_remnant].append(current_cutting)
            else:
                cutting_scheme[min_remnant] = [current_cutting]

            # Уберем использованный остаток и полученные изделия для следующих итераций
            if len(cutting_scheme[min_remnant]) == min_remnant[1]:
                current_remnants.remove(min_remnant)
            current_products = self.remove_list_from_array(current_products, current_cutting)
            # После распила могли остаться остатки, которые меньше всех оставшихся изделий - уберем их
            if len(current_products) >= 1:
                current_remnants = {remnant for remnant in current_remnants if remnant[0] >= min(current_products)}

        return cutting_scheme
