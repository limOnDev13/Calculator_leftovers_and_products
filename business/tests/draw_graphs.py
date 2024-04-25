from business.tests.test_algorithm import TestAllAlgorithm, TestAlgorithm
from business.quick_cutting import QuickCutting
from business.middle_cutting import MiddleCutting


if __name__ == '__main__':
    max_num_products: int = 60
    test_all_algorithms: TestAllAlgorithm = TestAllAlgorithm(
        algorithms=[QuickCutting, MiddleCutting],
        test_cls=TestAlgorithm,
        max_num_products=max_num_products
    )

    test_all_algorithms.draw_graphs_from_file('quick_middle_dependence.txt', 'quick_middle_graph.png', check_split=True)
