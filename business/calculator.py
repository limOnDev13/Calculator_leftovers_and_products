from random import uniform


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
        if result_min_rest > remnant - sum(current_selection):
            result_min_rest = remnant - sum(current_selection)
            result_selection = current_selection

    return result_selection


# number_products: int = 20
# rest: float = round(uniform(10, 20), 1)
# list_products: list[float] = [
#     round(uniform(1, 30), 1)
#     for _ in range(number_products)
# ]
# small_products: list[float] = [
#     product
#     for product in list_products
#     if product < rest
# ]
# print(f'rest = {rest}')
# print(f'products = {list_products}')
# print(f'small_products = {small_products}')
#
# print(f'Лучший рез: {min_rest_cutting(remnant=rest, products=list_products)}')
