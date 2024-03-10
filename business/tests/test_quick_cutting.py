"""
Модуль для тестирования метода calculator.quick_cutting
"""
from business.calculator import QuickCutting
import random


def print_result(products: list[float], rests: list[float]):
    quick_cutting: QuickCutting = QuickCutting(remnants=rests, products=products)
    res_dict: dict[tuple[float, int], list[list[float]]] = quick_cutting.cut()
    for remnant, opt_products in res_dict.items():
        print('{}: {}'.format(remnant, opt_products))


print('Случайные значения')
rand_products: list[float] = [round(random.uniform(0.1, 3.0), 3) for _ in range(random.randint(1, 20))]
rand_rests: list[float] = [round(random.uniform(0.1, 4.0), 3) for _ in range(random.randint(1, 20))]
print_result(rand_products, rand_rests)

print('\nТест 1')
products_test1: list[float] = [0.1, 0.1, 0.2, 0.3]
rests_test1: list[float] = [0.15, 0.15, 0.15, 0.4, 0.05]
print_result(products_test1, rests_test1)
