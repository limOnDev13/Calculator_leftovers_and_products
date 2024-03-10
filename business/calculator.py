from random import uniform
from copy import copy


class Cutting:
    """
    Базовый класс для расчета реза остатков под изделия

    Args:
        remnants (list[float]) - список ширин остатков профилей
        products (list[float]) - список ширин изделий, которые нужно получить
        cutting_width (float) - ширина реза
    """
    def __init__(self, remnants: list[float], products: list[float], cutting_width: float = 0.003) -> None:
        self.__remnants: list[float] = remnants
        self.__products: list[float] = products
        self.__cutting_width: float = cutting_width

    def get_remnants(self) -> list[float]:
        """
        Геттер для получения списка остатков
        :return: __remnants
        :rtype: list[float]
        """
        return self.__remnants

    def get_products(self) -> list[float]:
        """
        Геттер для получения списка изделий
        :return: __products
        :rtype: list[float]
        """
        return self.__products

    def get_cutting_width(self) -> float:
        """
        Геттер для получения ширины реза
        :return: __cutting_width
        :rtype: float
        """
        return self.__cutting_width

    def min_rest_cutting(self, remnant: float, products: list[float]) -> list[float]:
        """
        Функция рекурсивно перебирает все изделий для поиска наилучшего реза данного остатка
        :param remnant: Длина остатка
        :type remnant: float
        :param products: Список оставшихся изделий
        :type products: list[float]
        :return: Список ширин изделий, которые лучше всего использовать для данного остатка
        :rtype: list[float]
        """
        # Сначала соберем изделия, которые меньше длины остатков
        small_products: list[float] = [
            product
            for product in products
            if product < remnant - self.get_cutting_width()
        ]

        # Если small_products пустой или имеет один элемент, то это условие остановки рекурсии
        if len(small_products) <= 1:
            return small_products

        result_min_rest: float = remnant
        result_selection: list[float] = list()

        for num_product, product in enumerate(small_products):
            current_selection: list[float] = [product]
            current_selection.extend(self.min_rest_cutting(remnant=remnant - product - self.get_cutting_width(),
                                                           products=small_products[num_product + 1:]))

            # Если result_min_rest больше чем разность остатка и суммы выбранных длин, то выбор не эффективен
            if result_min_rest > remnant - sum(current_selection) - self.get_cutting_width() * len(current_selection):
                result_min_rest = remnant - sum(current_selection) - self.get_cutting_width() * len(current_selection)
                result_selection = current_selection

        return result_selection

    @staticmethod
    def remove_list_from_list(init_list: list[float], deleted_list: list[float]):
        """
        Функция удаляет все элементы deleted_list из init_list.
        :param init_list: Начальный список.
        :param deleted_list: Список элементов, которые нужно удалить.
        :return: Ничего, функция редактирует init_list.
        """
        for item in deleted_list:
            init_list.remove(item)

    def generate_keys(self) -> list[tuple[float, int]]:
        """
        Так как все методы расчета возвращают результат в одном и том же виде (в виде словаря),
        то у всех повторяется код генерации ключей для этого словаря. Этот метод генерирует ключи для выходного словаря.
        :return: Список ключей для выходного словаря
        :rtype: list[tuple[float, int]]
        """
        remnants: list[float] = self.get_remnants()

        return [
            # (ширина остатка, кол-во остатков с такой шириной)
            (remnant, remnants.count(remnant))
            for remnant in set(remnants)
        ]

    def cut(self) -> dict[tuple[float, int], list[list[float]]]:
        """
        Заготовка для функции реза
        :return: Словарь. Ключи - кортежи остатков, где float - ширина, int - кол-во остатков с такой шириной
        (кортежи взяты, чтобы решить проблему, если есть несколько остатков одной ширины); списки списков ширин изделий
        (если несколько остатков, то в список будет содержать несколько списков изделий).
        """
        pass


class QuickCutting(Cutting):
    """
    Класс - наследник Cutting для расчета реза остатков под изделия. Содержит в себе алгоритм быстрого расчета

    Args:
        remnants (list[float]) - список ширин остатков профилей
        products (list[float]) - список ширин изделий, которые нужно получить
        cutting_width (float) - ширина реза
    """

    def __init__(self, remnants: list[float], products: list[float], cutting_width: float = 0.003) -> None:
        super().__init__(remnants, products, cutting_width)

    def cut(self) -> dict[tuple[float, int], list[list[float]]]:
        """
        Функция производит быстрый расчет для реза списка остатков под изделия из списка. Для этого функция берет
        остатки по возрастанию и оптимально подбирает изделия.
        :return: Словарь. Ключи - кортежи остатков, где float - ширина, int - кол-во остатков с такой шириной
        (кортежи взяты, чтобы решить проблему, если есть несколько остатков одной ширины); списки списков ширин изделий
        (если несколько остатков, то в список будет содержать несколько списков изделий)
        :rtype: dict[tuple[float, int], list[list[float]]]
        """
        result_dict: dict[tuple[float, int], list[list[float]]] = dict()
        cur_products: list[float] = copy(self.get_products())

        # 1) сгенерируем список ключей
        keys: list[tuple[float, int]] = self.generate_keys()  # Список ключей для генерации словаря

        # 2) сгенерируем значения для ключей и словарь
        for tuple_remnant in sorted(keys, key=lambda x: x[0]):
            # если изделия закончились - выйдем из цикла
            if not cur_products:
                break
            # Если остаток меньше всех изделий, то пропустим итерацию
            if tuple_remnant[0] < min(cur_products):
                continue

            values: list[list[float]] = list()

            for _ in range(tuple_remnant[1]):
                # для каждого остатка одной ширины проведем оптимальный рез и добавим в список значений
                rest_cutting: list[float] = self.min_rest_cutting(tuple_remnant[0], cur_products)
                values.append(rest_cutting)
                # отрезанные изделия удалим из текущего списка изделий
                self.remove_list_from_list(cur_products, rest_cutting)
                # если изделия закончились - прервем цикл
                if not cur_products:
                    break
            result_dict[tuple_remnant] = values

        return result_dict


class MiddleCutting(Cutting):
    """
    Класс - наследник Cutting для расчета реза остатков под изделия. Содержит в себе алгоритм расчета
    (работает медленнее, чем QuickCutting, но более оптимально)

    Args:
        remnants (list[float]) - список ширин остатков профилей
        products (list[float]) - список ширин изделий, которые нужно получить
        cutting_width (float) - ширина реза
    """

    def __init__(self, remnants: list[float], products: list[float], cutting_width: float = 0.003) -> None:
        super().__init__(remnants, products, cutting_width)

    def cut(self) -> dict[tuple[float, int], list[list[float]]]:
        """
        Функция производит расчет со средней скоростью для реза списка остатков под изделия из списка.
        Для этого функция берет остаток, для которого рез будет наиболее оптимальным.
        И таким образом пробегает все остатки.
        :return: Словарь. Ключи - кортежи остатков, где float - ширина, int - кол-во остатков с такой шириной
        (кортежи взяты, чтобы решить проблему, если есть несколько остатков одной ширины); списки списков ширин изделий
        (если несколько остатков, то в список будет содержать несколько списков изделий)
        :rtype: dict[tuple[float, int], list[list[float]]]
        """
        result_dict: dict[tuple[float, int], list[list[float]]] = dict()
        cur_products: list[float] = copy(self.get_products())

        # 1) сгенерируем список ключей
        keys: list[tuple[float, int]] = self.generate_keys()  # Список ключей для генерации словаря
        # 1.1) сделаем вспомогательную копию
        cur_keys: list[tuple[float, int]] = copy(keys)

        # 2) В цикле будем искать остатки, для которых рез будет наиболее оптимальным. Если остатков одной длины
        # больше одного, то подбираем оптимальный рез для одного. Повторяем итерацию.
        # Если оптимальным снова станет остаток с той же длиной, то в значение словаря добавляем список
        while True:
            # Условие выхода их цикла
            if not cur_keys or not cur_products:
                break

            # Найдем оптимальный рез из списка оставшихся ключей и изделий
            min_rest: float = max(self.get_remnants())
            opt_remnant: tuple[float,  int] = (0.0, 0)
            opt_selection: list[float] = []
            for remnant in cur_keys:
                best_selection: list[float] = self.min_rest_cutting(remnant[0], cur_products)

                if remnant[0] - sum(best_selection) - self.get_cutting_width() * len(best_selection) < min_rest:
                    min_rest = remnant[0] - sum(best_selection) - self.get_cutting_width() * len(best_selection)
                    opt_remnant = remnant
                    opt_selection = best_selection

            # добавим в итоговый словарь найденные значения
            if opt_remnant in result_dict:
                result_dict[opt_remnant].append(opt_selection)
            else:
                result_dict[opt_remnant] = [opt_selection]

            # Если длина списка наборов равна количеству остатков данной длины,
            # то данный остаток удалим из текущего списка остатков
            if opt_remnant[1] == len(result_dict[opt_remnant]):
                cur_keys.remove(opt_remnant)
            # удалим из текущего списка изделий сохраненный список изделий
            self.remove_list_from_list(cur_products, opt_selection)

        return result_dict


class BestCutting(Cutting):
    """
    Класс - наследник Cutting для расчета реза остатков под изделия.
    Содержит в себе алгоритм самого оптимального расчета реза (суммарный остаток будет наименьшим).
    Главный минус алгоритма - его скорость. Скорость алгоритма сравнима с O(n! * m!),
    где n и m - количества остатков и изделий (алгоритм основан на переборе всевозможных комбинаций).

    Args:
        remnants (list[float]) - список ширин остатков профилей
        products (list[float]) - список ширин изделий, которые нужно получить
        cutting_width (float) - ширина реза
    """

    def __init__(self, remnants: list[float], products: list[float], cutting_width: float = 0.003) -> None:
        super().__init__(remnants, products, cutting_width)

    def cut(self) -> dict[tuple[float, int], list[list[float]]]:
        """
        Функция производит наилучший за счет перебора всевозможных комбинаций расчет для реза списка остатков
        под изделия из списка.
        :return: Словарь. Ключи - кортежи остатков, где float - ширина, int - кол-во остатков с такой шириной
        (кортежи взяты, чтобы решить проблему, если есть несколько остатков одной ширины); списки списков ширин изделий
        (если несколько остатков, то в список будет содержать несколько списков изделий)
        :rtype: dict[tuple[float, int], list[list[float]]]
        """
