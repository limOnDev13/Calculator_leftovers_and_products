"""
Модуль для тестирования метода QuickCutting.cut()
"""
from business.middle_cutting import MiddleCutting
from test_algorithm import TestAlgorithm
import random


# Инициализируем тестовый класс
test_middle_cutting: TestAlgorithm = TestAlgorithm(
    algorithm_cls=MiddleCutting,
    min_rest_length=1,
    whole_profile_length=6
)

print('Тест 1')
rand_products: list[float] = [round(random.uniform(0.1, 3.0), 3) for _ in range(random.randint(1, 20))]
rand_rests: list[float] = [round(random.uniform(0.1, 4.0), 3) for _ in range(random.randint(1, 20))]
print('Изделия:', rand_products)
print('Остатки:', rand_rests)
result_cut: dict[tuple[float, int], list[list[float]]] = test_middle_cutting.test_selection(rand_products, rand_rests)
print(test_middle_cutting.beautiful_result(result_cut))
print('Процент отхода: {percent}%'.format(percent=test_middle_cutting.calculate_waste(result_cut)))

print('\nТест 2')
products_test1: list[float] = [0.1, 0.1, 0.2, 0.3]
rests_test1: list[float] = [0.15, 0.15, 0.15, 0.4, 0.05]
print('Изделия:', products_test1)
print('Остатки:', rests_test1)
result_cut = test_middle_cutting.test_selection(products_test1, rests_test1)
print(test_middle_cutting.beautiful_result(result_cut))
print('Процент отхода: {percent}%'.format(percent=test_middle_cutting.calculate_waste(result_cut)))

print('Тест 3')
rand_products: list[float] = [round(random.uniform(1, 6), 3) for _ in range(60)]
rand_rests: list[float] = [round(random.uniform(1, 6), 3) for _ in range(random.randint(1, 10))]
rand_rests.extend([6 for _ in range(60)])
print('Изделия:', rand_products)
print('Остатки:', rand_rests)
result_cut = test_middle_cutting.test_selection(rand_products, rand_rests)
print(test_middle_cutting.beautiful_result(result_cut))
print('Процент отхода: {percent}%'.format(percent=test_middle_cutting.calculate_waste(result_cut)))
