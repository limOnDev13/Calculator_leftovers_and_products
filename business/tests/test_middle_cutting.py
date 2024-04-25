"""
Модуль для тестирования метода calculator.quick_cutting
"""
import random
from business.cutting import Cutting
from typing import Type
from business.middle_cutting import MiddleCutting
import time
import matplotlib.pyplot as plt


def print_result(products: list[float], rests: list[float],
                 cutting_class: Type[Cutting]) -> dict[tuple[float, int], list[list[float]]]:
    """
    Функция для красивой печати результатов
    :param products: Список продуктов
    :type products: list[float]
    :param rests: Список остатков
    :type rests: list[float]
    :param cutting_class: Тестируемый класс
    :type cutting_class: Type[Cutting]
    :return: Рассчитанный распил
    :rtype: dict[tuple[float, int], list[list[float]]]
    """
    middle_cutting: Cutting = cutting_class(
        remnants=rests,
        products=products,
        number_whole_profiles=len(products))
    res_dict: dict[tuple[float, int], list[list[float]]] = middle_cutting.cut()
    for remnant, opt_products in res_dict.items():
        # print(f'{remnant}:'.format(remnant, opt_products, round(remnant[0] - sum(opt_products[0]), 3)))
        print(f'{remnant}:')
        for opt_product in opt_products:
            print(f'\t{opt_product} = {round(sum(opt_product), 3)}'
                  f' ({remnant[0]}, ост: {round(remnant[0] - sum(opt_product), 3)})')

    return res_dict


def beautiful_result(cutting_scheme: dict[tuple[float, int], list[list[float]]]) -> str:
    """
    Функция преобразует схему распила в удобно читаемый текст
    :param cutting_scheme: Схема распила
    :type cutting_scheme: dict[tuple[float, int], list[list[float]]]
    :return: Строковое представление распила
    :rtype: str
    """
    result_string: str = ''

    for remnant, opt_products in cutting_scheme.items():
        result_string += f'{remnant}:\n'
        for opt_product in opt_products:
            result_string += (f'\t{opt_product} = {round(sum(opt_product), 3)} '
                              f'({remnant[0]}, ост: {round(remnant[0] - sum(opt_product), 3)})\n')

    return result_string


def testing_cutting_func(cutting_class: Type[Cutting],
                         num_tests: int, num_products: int, random_limit_rest: int,
                         whole_profile_length: float = 4.0, min_rest_length: float = 0.3,
                         print_progress: bool = False, print_full_info: bool = False,) -> float:
    """
    Метод генерирует num_tests тестов с num_products шт случайных изделий, добавляя к ним случайное число
    (не больше random_limit_rests) имеющихся остатков и возвращает среднее арифметическое процентов отхода
    :param cutting_class: Тестируемый класс расчета распила
    :type cutting_class: Type[Cutting]
    :param num_tests: Количество тестов
    :type num_tests: int
    :param num_products: Количество случайных изделий
    :type num_products: int
    :param random_limit_rest: Предел случайного количества имеющихся остатков
    :type random_limit_rest: int
    :param whole_profile_length: длина целого профиля
    :type whole_profile_length: float
    :param min_rest_length: Минимальная длина остатка. В отход идут остатки, меньше этой длины
    :type min_rest_length: float
    :param print_progress: Если True, то будет писать какой по счету проводится тест
    :type print_progress: bool
    :param print_full_info: Если True, то будет писать подробную информацию о каждом распиле
    :type print_full_info: bool
    :return: Средний процент отхода
    :rtype: float
    """
    average_waste: float = 0.0

    for test in range(num_tests):
        if print_progress:
            print(f'Тест {test + 1}/{num_tests}')
        # Сгенерируем начальные данные
        random_products: list[float] = [round(random.uniform(min_rest_length, whole_profile_length), 3)
                                        for _ in range(num_products)]
        random_rests: list[float] = [round(random.uniform(min_rest_length, whole_profile_length), 3)
                                     for _ in range(random.randint(0, random_limit_rest))]
        # Добавим цельных материалов в количестве изделий, чтобы хватило наверняка
        random_rests.extend([whole_profile_length for _ in range(num_products)])

        # Посчитаем распил
        middle_cutting: Cutting = cutting_class(
            remnants=random_rests,
            products=random_products,
            number_whole_profiles=num_products)
        if print_full_info:
            print('Список изделий: {products}\nСписок остатков: {rests}\n'.format(
                products=random_products,
                rests=random_rests
            ))
        res_dict: dict[tuple[float, int], list[list[float]]] = middle_cutting.cut()

        # Если нужно, распечатаем распил
        if print_full_info:
            print('Распил:\n{cutting_scheme}'.format(cutting_scheme=beautiful_result(res_dict)))

        # Посчитаем суммарный расход данного распила
        current_waste: float = 0.0
        used_leftovers: float = 0.0

        for remnant, lists_products in res_dict.items():
            for products in lists_products:
                if len(products) != 0:
                    used_leftovers += remnant[0]

                    rest: float = remnant[0] - sum(products)
                    if rest < min_rest_length:
                        current_waste += rest

        percentage_waste: float = round(current_waste * 100 / used_leftovers, 3)

        if print_progress:
            print(f'Отход в данном тесте: {percentage_waste}%\n')
        average_waste += percentage_waste

    return round(average_waste / num_tests, 3)


# print('Средний отход за все тесты: {}%'.format(
#     testing_cutting_func(
#         cutting_class=MiddleCutting,
#         num_tests=100,
#         num_products=20,
#         random_limit_rest=10,
#         min_rest_length=1,
#         whole_profile_length=6,
#         print_progress=True, print_full_info=True)))

max_number_products: int = 60
number_tests: int = 1000
func_graph: dict[int, float] = dict()
for number_products in range(1, max_number_products + 1):
    start_time: float = time.time()
    func_graph[number_products] = testing_cutting_func(
        cutting_class=MiddleCutting,
        num_tests=number_tests,
        num_products=number_products,
        random_limit_rest=10,
        min_rest_length=1,
        whole_profile_length=6,
        print_progress=False, print_full_info=False)
    print(f'{number_products}: {func_graph[number_products]} - {round((time.time() - start_time) / number_tests, 3)} c')

with open(f'{number_tests}test-{max_number_products}products.txt', 'w', encoding='utf-8') as file:
    for num, per in func_graph.items():
        print(f'{num}: {per}')
        file.write(f'{num}: {per}\n')
plt.plot(list(func_graph.keys()), list(func_graph.values()))
plt.show()
