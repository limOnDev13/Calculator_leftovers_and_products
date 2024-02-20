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


def remove_list_from_list(init_list: list[float], deleted_list: list[float]):
    """
    Функция удаляет все элементы deleted_list из init_list.
    :param init_list: Начальный список.
    :param deleted_list: Список элементов, которые нужно удалить.
    :return: Ничего, функция редактирует init_list.
    """
    for item in deleted_list:
        init_list.remove(item)


def quick_cutting(remnants: list[float], products: list[float], cutting_width: float = 0.003
                  ) -> dict[tuple[float, int], list[list[float]]]:
    """
    Функция производит быстрый расчет для реза списка остатков под изделия из списка. Для этого функция берет
    остатки по возрастанию и оптимально подбирает изделия.
    :param remnants: Список остатков.
    :param products: Список изделий.
    :param cutting_width: Ширина реза.
    :return: Словарь. Ключи - кортежи остатков, где float - ширина, int - кол-во остатков с такой шириной
    (кортежи взяты, чтобы решить проблему, если есть несколько остатков одной ширины); списки списков ширин изделий
    (если несколько остатков, то в список будет содержать несколько списков изделий).
    """
    result_dict: dict[tuple[float, int], list[list[float]]] = dict()
    cur_products: list[float] = copy(products)

    # 1) сгенерируем список ключей
    keys: list[tuple[float, int]] = [
        # (ширина остатка, кол-во остатков с такой шириной)
        (remnant, remnants.count(remnant))
        for remnant in set(remnants)
    ]  # Список ключей для генерации словаря

    # 2) сгенерируем значения для ключей и словарь
    for tuple_remnant in sorted(keys, key=lambda x: x[0]):
        # если изделия закончились - выйдем из цикла
        if not cur_products:
            break

        values: list[list[float]] = list()

        for _ in range(tuple_remnant[1]):
            # для каждого остатка одной ширины проведем оптимальный рез и добавим в список значений
            rest_cutting: list[float] = min_rest_cutting(tuple_remnant[0], cur_products, cutting_width)
            values.append(rest_cutting)
            # отрезанные изделия удалим из текущего списка изделий
            remove_list_from_list(cur_products, rest_cutting)
            # если изделия закончились - прервем цикл
            if not cur_products:
                break
        result_dict[tuple_remnant] = values

    return result_dict
