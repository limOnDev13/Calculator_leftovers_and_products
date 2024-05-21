"""
Модуль для тестирования метода business.best_cutting.BestCutting.cut()
"""
from business.best_cutting import BestCutting
import random
from test_algorithm import TestAlgorithm


test_best_cut: TestAlgorithm = TestAlgorithm(algorithm_cls=BestCutting)

# Тест - кол-во изделий = 10, кол-во остатков = 5
products: list[float] = [round(random.uniform(1, 6), 3) for _ in range(10)]
remnants: list[float] = [round(random.uniform(1, 6), 3) for _ in range(5)]
remnants.extend([6 for _ in range(10)])

best_cut: BestCutting = BestCutting(remnants=remnants, products=products, number_whole_profiles=100)
test_best_cut.beautiful_result(best_cut.cut())
