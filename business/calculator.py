from random import uniform
from copy import copy


def min_rest_cutting(remnant: float, products: list[float], cutting_width: float = 0.003) -> list[float]:
    """
    Функция рекурсивно перебирает все остатки для поиска наилучшего реза.
    :param remnant: Длина остатка.
    :param products: Список ширин изделий.
    :param cutting_width: Ширина реза.
    :return: Список ширин изделий, которые лучше всего использовать для данного остатка
    """
    # Сначала соберем изделия, которые меньше длины остатков
    small_products: list[float] = [
        product
        for product in products
        if product < remnant
    ]

    # Если small_products пустой или имеет один элемент, то это условие остановки рекурсии
    if len(small_products) <= 1:
        return small_products

    result_min_rest: float = remnant
    result_selection: list[float] = list()

    for num_product, product in enumerate(small_products):
        current_selection: list[float] = [product]
        current_selection.extend(min_rest_cutting(remnant=remnant - product - cutting_width,
                                                  products=small_products[num_product + 1:]))

        # Если result_min_rest больше чем разность остатка и суммы выбранных длин, то выбор не эффективен
        if result_min_rest > remnant - sum(current_selection) - cutting_width * len(current_selection):
            result_min_rest = remnant - sum(current_selection) - cutting_width * len(current_selection)
            result_selection = current_selection

    return result_selection


def remove_elements_from_list(list_nums: list[float], elements: list[float]) -> list[float]:
    """
    Удаляет из list_nums элементы elements и возвращает результатный список.
    :param list_nums: Список чисел.
    :param elements: Список чисел, которые нужно удалить.
    :return: Список полученных чисел.
    """
    return [
        num
        for num in list_nums
        if num not in elements
    ]


def quick_cutting(remnants: list[float], products: list[float], cutting_width: float) -> dict[float, list[float]]:
    """
    Функция для быстрого поиска лучшего реза. Функция берет остатки по возрастанию и для каждого из них ищет оптимальный
    рез.
    :param remnants: Список остатков.
    :param products: Список ширин изделий.
    :param cutting_width: Ширина реза.
    :return: Словарь с результатом. Ключ - ширина остатка, значение - список изделий под этот рез.
    """
    result_dict: dict[float, list[float]] = dict()
    current_products: list[float] = copy(products)

    # Будем брать остатки по возрастанию
    for remnant in sorted(remnants):
        # Для каждого остатка применим функцию min_rest_cutting со списком оставшихся изделий
        result_dict[remnant] = min_rest_cutting(remnant=remnant, products=current_products, cutting_width=cutting_width)
        # Из текущего списка изделий удалим уже подобранные.
        current_products = remove_elements_from_list(current_products, result_dict[remnant])

        # Если изделия закончились, прервем цикл
        if len(current_products) == 0:
            break

    return result_dict


# number_products: int = 10
# number_rests: int = 20
#
# rests: list[float] = [round(uniform(30, 40), 2) for _ in range(number_rests)]
# products: list[float] = [round(uniform(10, 20), 2) for _ in range(number_products)]
#
# result_dict: dict[float, list[float]] = quick_cutting(rests, products, cutting_width=0.05)
# for key, value in result_dict.items():
#     print('{}: {}, ост: {}'.format(key, value, round(key - sum(value), 3)))
