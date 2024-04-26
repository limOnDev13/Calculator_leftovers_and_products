from business.cutting import Cutting
from copy import deepcopy
from typing import Optional


class MiddleCutting(Cutting):
    __name__ = 'MiddleCutting'

    def __str__(self) -> str:
        return ('Данный метод сначала ищет остаток, для которого распил будет оптимальным,'
                ' и так по очереди рассчитывает распил для всех изделий')

    def cut(self) -> dict[tuple[float, int], list[list[float]]]:
        """
        Метод для расчета распила. Данный метод сначала ищет остаток, для которого распил будет оптимальным,
        и так по очереди рассчитывает распил для всех изделий
        :return: Распил. Имеет тип словаря, ключи - кортежи, где первый элемент - длина остатка,
        второй - количество остатков данной длины. Значения словаря - список списков изделий для одного такого остатка
        :rtype: dict[tuple[float, int], list[list[float]]]
        """
        cutting_scheme: dict[tuple[float, int], list[list[float]]] = dict()
        current_remnants: set[tuple[float, int]] = self.generate_keys(self.remnants, min(self.products))
        current_products: list[float] = deepcopy(self.products)

        while current_products and current_remnants:
            # Найдем остаток, для которого распил будет самым оптимальным
            min_waste: float = self.whole_profile_length
            best_remnant: Optional[tuple[float, int]] = None
            best_cutting: list[float] = list()

            for remnant in current_remnants:
                current_cutting: list[float] = self.calculate_min_waste(remnant[0], current_products)
                waste = remnant[0] - sum(current_cutting) - len(current_cutting) * self.cutting_width
                if waste < min_waste:
                    min_waste = waste
                    best_remnant = remnant
                    best_cutting = current_cutting

            # Добавим его в итоговый словарь
            if best_remnant in cutting_scheme:
                cutting_scheme[best_remnant].append(best_cutting)
            else:
                cutting_scheme[best_remnant] = [best_cutting]

            # Уберем использованный остаток и полученные изделия для следующих итераций
            if len(cutting_scheme[best_remnant]) == best_remnant[1]:
                current_remnants.remove(best_remnant)
            current_products = self.remove_list_from_array(current_products, best_cutting)
            # Некоторые остатки могут быть меньше всех оставшихся изделий - их тоже уберем
            if len(current_products) >= 1:
                current_remnants = {remnant for remnant in current_remnants if remnant[0] >= min(current_products)}

        return cutting_scheme
