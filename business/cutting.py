from copy import deepcopy
from abc import ABC, abstractmethod
from typing import Literal


class Cutting(ABC):
    """
    Базовый класс для расчета распила

    Args:
        remnants (list[float]) - список остатков
        products (list[float]) - список изделий
       Rewrote the Cutting module number_whole_profiles (int) - количество цельных профилей
        cutting_width (float) - ширина реза
        whole_profile_length (float) - длина цельного профиля
        min_rest_length (float) - Минимальная длина остатка. Остатки меньше - отход
    """
    def __init__(self, *, remnants: list[float], products: list[float], number_whole_profiles: int,
                 cutting_width: float = 0.003, whole_profile_length: float = 6.0,
                 min_rest_length: float = 1.0) -> None:
        self.__remnants: list[float] = remnants
        self.__products: list[float] = products
        self.__number_whole_profiles: int = number_whole_profiles
        self.__cutting_width: float = cutting_width
        self.__whole_profile_length: float = whole_profile_length
        self.__min_rest_length: float = min_rest_length

    @property
    def remnants(self) -> list[float]:
        """Геттер для self.__remnants"""
        return self.__remnants

    @property
    def products(self) -> list[float]:
        """Геттер для self.__products"""
        return self.__products

    @property
    def cutting_width(self) -> float:
        """Геттер для self.__cutting_width"""
        return self.__cutting_width

    @property
    def whole_profile_length(self) -> float:
        """Геттер для self.__whole_profile_length"""
        return self.__whole_profile_length

    @property
    def min_rest_length(self) -> float:
        """Геттер для self.__min_rest_length"""
        return self.__min_rest_length

    def calculate_min_waste(self, remnant: float, products: list[float]) -> list[float]:
        """
        Метод ищет оптимальный распил для данного остатка на данный список изделий
        :param remnant: Длина остатка
        :param remnant: float
        :param products: Список изделий, на которые можно пустить остаток
        :type products: list[float]
        :return: Распил данного остатка
        :rtype: list[float]
        """
        # 1) Удалим все изделия, длиннее остатка
        current_products: list[float] = [product for product in products if product <= remnant]

        # 2) Пробежимся по всем остаткам и рекурсивно найдем лучший рез
        min_waste: float = self.whole_profile_length
        result_cutting: list[float] = list()

        for product in current_products:
            current_cutting: list[float] = [product]
            copy_current_products = deepcopy(current_products)
            copy_current_products.remove(product)

            current_cutting.extend(self.calculate_min_waste(
                remnant=remnant - product - self.cutting_width,
                products=copy_current_products
            ))

            waste = remnant - sum(current_cutting) - len(current_cutting) * self.cutting_width
            if waste < min_waste:
                result_cutting = current_cutting
                min_waste = waste

        return result_cutting

    @abstractmethod
    def cut(self) -> dict[tuple[float, int], list[list[float]]]:
        """
        Метод для расчета распила
        :return: Распил. Имеет тип словаря, ключи - кортежи, где первый элемент - длина остатка,
        второй - количество остатков данной длины. Значения словаря - список списков изделий для одного такого остатка
        :rtype: dict[tuple[float, int], list[list[float]]]
        """
        pass

    @classmethod
    def generate_keys(cls, array: list[float], min_value: float) -> set[tuple[float, int]]:
        """
        Метод разбивает список на множество кортежей, в которых первый элемент - элемент списка,
        второй - количество одинаковых с ним элементов
        :param array: Список элементов
        :type array: list[float]
        :param min_value: Минимальное значение, элементы меньше него не попадут в результат
        :type min_value: float
        :return: Хистограмму элементов в списке
        :rtype: set[tuple[float, int]]
        """
        set_array: set[float] = set(array)
        return {(elem, array.count(elem)) for elem in set_array if elem >= min_value}

    @classmethod
    def remove_list_from_array(cls, init_array: list, removed_list: list) -> list:
        """
        Метод удаляет все элементы removed_array из init_array
        :param init_array: Начальный список
        :type init_array: list
        :param removed_list: Удаляемый список
        :type removed_list: list
        :return: Отредактированный начальный список
        :rtype: list
        """
        return [element for element in init_array if element not in removed_list]


if __name__ == '__main__':
    # Проверка Cutting.calculate_min_waste
    remnant: float = 0.01
    remnants: list[float] = [5.999, 3.252, 3.635, 5.691, 2.874]
    products: list[float] = [4.586, 1.962, 4.552, 2.164, 1.255, 4.587, 6, 6, 6, 6, 6, 0.5, 0.4, 1.1]
    cutting: Cutting = Cutting(remnants=remnants, products=products, number_whole_profiles=5)
    print(cutting.calculate_min_waste(remnant, products))