"""
Модуль для тестирования метода QuickCutting.cut()
"""
from business.quick_cutting import QuickCutting
from test_algorithm import TestAlgorithm
import random


# Инициализируем тестовый класс
test_quick_cutting: TestAlgorithm = TestAlgorithm(
    algorithm_cls=QuickCutting,
    min_rest_length=0.005,
    whole_profile_length=6
)

print('Случайные значения')
rand_products: list[float] = [round(random.uniform(0.1, 3.0), 3) for _ in range(random.randint(1, 20))]
rand_rests: list[float] = [round(random.uniform(0.1, 4.0), 3) for _ in range(random.randint(1, 20))]
print('Изделия:', rand_products)
print('Остатки:', rand_rests)
test_quick_cutting.test_selection(rand_products, rand_rests)

print('\nТест 1')
products_test1: list[float] = [0.1, 0.1, 0.2, 0.3]
rests_test1: list[float] = [0.15, 0.15, 0.15, 0.4, 0.05]
print('Изделия:', products_test1)
print('Остатки:', rests_test1)
test_quick_cutting.test_selection(products_test1, rests_test1)

test_quick_cutting.percentage_waste(max_number_products=60, number_tests=1000, print_terminal=True)
