from business.cutting import Cutting
from copy import deepcopy
from itertools import permutations
from typing import Optional


class BestCutting(Cutting):
    """
    Класс для расчета наилучшего распила.
    """
    def cut(self) -> dict[tuple[float, int], list[list[float]]]:
        """
        Метод для расчета распила. Алгоритм перебирает всевозможные распилы и выбирает тот,
        в котором процент отхода меньше всего
        :return: Распил. Имеет тип словаря, ключи - кортежи, где первый элемент - длина остатка,
        второй - количество остатков данной длины. Значения словаря - список списков изделий для одного такого остатка
        :rtype: dict[tuple[float, int], list[list[float]]]
        """
        cutting_scheme: dict[tuple[float, int], list[list[float]]] = dict()
        current_remnants: list[float] = [remnant for remnant in self.remnants if remnant > min(self.products)]
        # Вся загвоздка заключается в порядке использования остатков.
        # Поэтому сгенерируем всевозможные перестановки остатков
        all_permutations: list[tuple[float, ...]] = list(permutations(current_remnants))

        # Для каждого порядка посчитаем процент отхода
        min_percentage_waste: float = 100.0
        best_permutation: Optional[tuple[float, ...]] = None

        for permutation in all_permutations:
            waste: float = 0.0
            current_products: list[float] = deepcopy(self.products)
            used_remnants: list[float] = list()  # Список использованных остатков

            for remnant in permutation:
                # Если список изделий пуст, дальше проводить расчеты бессмысленно
                if not current_products:
                    break

                # Если остаток меньше всех изделий - считать под него распил бессмысленно,
                # иначе - добавим в список использованных остатков
                if remnant < min(current_products):
                    continue
                else:
                    used_remnants.append(remnant)

                current_cut: list[float] = self.calculate_min_waste(remnant=remnant, products=current_products)
                # Если остаток (с учетом отпиленной стружки) меньше, чем длина минимального остатка - это отход
                if self.min_rest_length > remnant - sum(current_cut) - self.cutting_width * len(current_cut):
                    waste += remnant - sum(current_cut)

                # Удалим из списка изделий уже полученные
                current_products = self.remove_list_from_array(current_products, current_cut)

            # Посчитает процент отхода
            total_material: float = sum(used_remnants)
            total_products: float = sum(self.products)
            percentage_waste: float = round((total_material - total_products) / total_material * 100, 3)

            if percentage_waste < min_percentage_waste:
                min_percentage_waste, best_permutation = percentage_waste, tuple(used_remnants)

        # Найдя лучший распил, соберем схему распила. Пока в отдельном цикле, после можно перенести в предыдущий,
        # чтобы не делать лишних итераций
        keys: set[tuple[float, int]] = self.generate_keys(list(best_permutation), 0.0)
        current_products: list[float] = deepcopy(self.products)

        for remnant in best_permutation:
            # Найдем нужный ключ
            required_key: Optional[tuple[float, int]] = None

            for key in keys:
                if key[0] == remnant:
                    required_key = key
                    break

            if required_key in cutting_scheme:
                cutting_scheme[required_key].append(self.calculate_min_waste(required_key[0], current_products))
            else:
                cutting_scheme[required_key] = [self.calculate_min_waste(required_key[0], current_products)]

            # Удалим из текущих изделий последний добавленный список по ключу required_key
            current_products = self.remove_list_from_array(current_products, cutting_scheme[required_key][-1])
