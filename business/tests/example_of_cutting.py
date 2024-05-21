import random

from business.tests.test_algorithm import TestAlgorithm
from business.middle_cutting import MiddleCutting
from business.quick_cutting import QuickCutting


min_length_remnants: float = 1
whole_profile_length: float = 6

test_mc: TestAlgorithm = TestAlgorithm(algorithm_cls=MiddleCutting,
                                       min_rest_length=min_length_remnants,
                                       whole_profile_length=whole_profile_length)
test_qc: TestAlgorithm = TestAlgorithm(algorithm_cls=QuickCutting,
                                       min_rest_length=min_length_remnants,
                                       whole_profile_length=whole_profile_length)

max_num_products: int = 70
step_num_products: int = 10
step_num_remnants: int = 10

with open('example_cutting.txt', 'w', encoding='utf-8') as example:
    for num_products in range(step_num_products, max_num_products, step_num_products):
        for num_remnants in range(0, num_products + step_num_remnants, step_num_remnants):
            example.write(f'Пример - {num_products} случайных изделий; {num_remnants} случайных остатков\n')
            products: list[float] = [round(random.uniform(min_length_remnants, whole_profile_length), 3)
                                     for _ in range(num_products)]
            remnants: list[float] = [round(random.uniform(min_length_remnants, whole_profile_length), 3)
                                     for _ in range(num_remnants)]
            remnants.extend([whole_profile_length for _ in range(num_products)])

            example.write(f'Изделия: {products}\nОстатки: {remnants}\n')
            example.write('Распил с помощью алгоритма QuickCutting:\n')
            qc_cut = test_qc.test_selection(products, remnants)
            example.write(f'{test_qc.beautiful_result(qc_cut)}')
            example.write(f'Отход: {test_qc.calculate_waste(qc_cut)}%\n\n')

            example.write('Распил с помощью алгоритма MiddleCutting:\n')
            mc_cut = test_mc.test_selection(products, remnants)
            example.write(f'{test_qc.beautiful_result(mc_cut)}')
            example.write(f'Отход: {test_mc.calculate_waste(mc_cut)}%\n\n')
            example.write('--------------------------------------------\n\n')
