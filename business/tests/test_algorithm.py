import random
from typing import Type
import time
import matplotlib.pyplot as plt

from business.cutting import Cutting
from business.middle_cutting import MiddleCutting
from business.quick_cutting import QuickCutting


class TestAlgorithm:
    """
    Класс для тестирования алгоритмов расчета распила

    Args:
        algorithm_cls (Type[Cutting]) - Класс с методом расчета раскроя
        min_rest_length (float) - Минимальная длина остатка
        whole_profile_length (float) - Длина целого профиля
    """
    def __init__(self, algorithm_cls: Type[Cutting], min_rest_length: float = 1, whole_profile_length: float = 6):
        self.__algorithm: Type[Cutting] = algorithm_cls
        self.__min_rest_length: float = min_rest_length
        self.__whole_profile_length: float = whole_profile_length

    @classmethod
    def beautiful_result(cls, cutting_scheme: dict[tuple[float, int], list[list[float]]]) -> str:
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

    def test_selection(self, products: list[float], rests: list[float],
                       print_result: bool = False) -> dict[tuple[float, int], list[list[float]]]:
        """
        Функция тестирует определенную выборку и выводит распил в терминал
        :param products: Список продуктов
        :type products: list[float]
        :param rests: Список остатков
        :type rests: list[float]
        :return: Рассчитанный распил
        :rtype: dict[tuple[float, int], list[list[float]]]
        """
        # Сделаем расчет распила
        cutting_object: Cutting = self.__algorithm(
            remnants=rests,
            products=products,
            number_whole_profiles=len(products),
            min_rest_length=self.__min_rest_length,
            whole_profile_length=self.__whole_profile_length
        )
        res_dict: dict[tuple[float, int], list[list[float]]] = cutting_object.cut()

        if print_result:
            print(self.beautiful_result(res_dict))

        return res_dict

    def calculate_waste(self, cutting_scheme: dict[tuple[float, int], list[list[float]]]) -> float:
        """
        Метод рассчитывает процент отхода в распиле
        :param cutting_scheme: Схема распила
        :type cutting_scheme: dict[tuple[float, int], list[list[float]]]
        :return: Процент отхода
        :rtype: float
        """
        # Посчитаем суммарный расход данного распила
        current_waste: float = 0.0
        used_leftovers: float = 0.0

        for remnant, lists_products in cutting_scheme.items():
            for products in lists_products:
                if len(products) != 0:
                    used_leftovers += remnant[0]

                    rest: float = remnant[0] - sum(products)
                    if rest < self.__min_rest_length:
                        current_waste += rest

        return round(current_waste * 100 / used_leftovers, 3)

    def testing_cutting_func(self, num_tests: int, num_products: int, random_limit_rest: int,
                             print_progress: bool = False, print_full_info: bool = False, ) -> float:
        """
        Метод генерирует num_tests тестов с num_products шт случайных изделий, добавляя к ним случайное число
        (не больше random_limit_rests) имеющихся остатков и возвращает среднее арифметическое процентов отхода
        :param num_tests: Количество тестов
        :type num_tests: int
        :param num_products: Количество случайных изделий
        :type num_products: int
        :param random_limit_rest: Предел случайного количества имеющихся остатков
        :type random_limit_rest: int
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
            random_products: list[float] = [round(random.uniform(
                self.__min_rest_length, self.__whole_profile_length), 3)
                                            for _ in range(num_products)]
            random_rests: list[float] = [round(random.uniform(self.__min_rest_length, self.__whole_profile_length), 3)
                                         for _ in range(random.randint(0, random_limit_rest))]
            # Добавим цельных материалов в количестве изделий, чтобы хватило наверняка
            random_rests.extend([self.__whole_profile_length for _ in range(num_products)])

            # Посчитаем распил
            middle_cutting: Cutting = self.__algorithm(
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
                print('Распил:\n{cutting_scheme}'.format(cutting_scheme=self.beautiful_result(res_dict)))

            percentage_waste: float = self.calculate_waste(res_dict)

            if print_progress:
                print(f'Отход в данном тесте: {percentage_waste}%\n')
            average_waste += percentage_waste

        return round(average_waste / num_tests, 3)

    def dependence_percentage_waste(self, max_number_products: int = 60, number_tests: int = 1000,
                                    print_terminal: bool = False) -> dict[int, float]:
        """
        Метод рассчитывает зависимость среднего процента отхода от количества изделий и сохраняет в файл.
        Файл будет иметь имя {название алгоритма}_{кол-во тестов на одно количество}_{максимальное кол-во тестов}.txt.
        Если такой файл уже есть, он будет перезаписан.
        :param max_number_products: Предел количества изделий.
        Тестирование будет проходить от 1 изделия до max_number_products
        :type max_number_products: int
        :param number_tests: Количество тестов на каждое количество изделий.
        Результат будет усредняться по этому количеству тестов, чем оно больше, тем результат точнее,
        но время работы программы больше
        :type number_tests: int
        :param print_terminal: Если True, результат будет дублироваться в терминал
        :type print_terminal: bool
        :return: Словарь зависимости
        :rtype: dict[int, float]
        """
        func_graph: dict[int, float] = dict()  # Зависимость будем хранить в виде словаря

        # Сделаем расчеты
        for number_products in range(1, max_number_products + 1):
            start_time: float = time.time()
            func_graph[number_products] = self.testing_cutting_func(
                num_tests=number_tests,
                num_products=number_products,
                random_limit_rest=10,
                print_progress=False, print_full_info=False)

            # Если нужно - запишем в терминал
            if print_terminal:
                print(f'{number_products}: {func_graph[number_products]}'
                      f' - {round((time.time() - start_time) / number_tests, 3)} c')

        # Сохраним результат в файл
        with open('{name}_{num_tests}_{max_num_products}.txt'.format(
            name=self.__algorithm.__name__,
            num_tests=number_tests,
            max_num_products=max_number_products
        ), 'w', encoding='utf-8') as file:
            for num, per in func_graph.items():
                print(f'{num}: {per}')
                file.write(f'{num}: {per}\n')

        return func_graph


class TestAllAlgorithm:
    """
    Класс для тестирования всех алгоритмов на одинаковых случайных выборках и для визуализации этих тестов

    Args:
        algorithms (list[Type[Cutting]]) - Список классов с алгоритмами для тестирования
        test_cls (Type[TestAlgorithm]) - Класс для тестирования одного алгоритма
        number_tests (int) - Количество тестов на одно количество изделий
        max_num_products (int) - Максимальное количество изделий.
        Тестирование будет проходить от 1 изделия до max_num_products
    """
    def __init__(self, *, algorithms: list[Type[Cutting]],
                 test_cls: Type[TestAlgorithm] = TestAlgorithm,
                 number_tests: int = 1000, max_num_products: int = 60):
        self.__algorithms: list[Type[Cutting]] = algorithms
        self.__test: Type[TestAlgorithm] = test_cls
        self.__number_tests: int = number_tests
        self.__max_num_products: int = max_num_products

    @property
    def test(self) -> Type[TestAlgorithm]:
        return self.__test

    def test_all_algorithms(self, products: list[float], remnants: list[float],
                            print_cut: bool = False) -> list[tuple[str, float]]:
        """
        Метод тестирует все алгоритмы на одинаковой выборке и выводит словарь с результатами
        :param products: Список изделий
        :type products: list[float]
        :param remnants: Список остатков
        :type remnants: list[float]
        :param print_cut: Если True, то напечатает в терминал раскрой каждого алгоритма и время работы
        :return: Список кортежей с результатами. Первый элемент кортежа - имя алгоритма, второе - процент отхода
        :rtype: list[tuple[str, float]]
        """
        algorithm_wastes: list[tuple[str, float]] = list()

        # Пройдемся по все алгоритмам
        for algorithm in self.__algorithms:
            test: TestAlgorithm = self.__test(algorithm)

            if print_cut:
                print(f'Тест алгоритма {algorithm.__name__}')

            # Посчитаем распил
            start_time: float = time.time()
            cutting_cheme: dict[tuple[float, int], list[list[float]]] = test.test_selection(products=products,
                                                                                            rests=remnants,
                                                                                            print_result=print_cut)
            # Сохраним результат
            waste: float = test.calculate_waste(cutting_cheme)
            algorithm_wastes.append((algorithm.__name__, waste))

            if print_cut:
                print(f'Процент отхода: {waste}%')
                print(f'Время работы: {round(time.time() - start_time, 4)}с\n')

        return algorithm_wastes

    def dependence_different_algorithms(self, whole_profile_length: float = 6,
                                        min_remnant_length: float = 1, limit_num_rests: int = 10,
                                        print_progress: bool = False, print_cut: bool = False
                                        ) -> dict[str, dict[int, float]]:
        """
        Метод рассчитывает зависимости процента отхода от количества изделий в разных алгоритмах
        :param whole_profile_length: Длина целого профиля
        :type whole_profile_length: float
        :param min_remnant_length: Минимальная длина остатка
        :type min_remnant_length: float
        :param limit_num_rests: Предел случайного количества остатков
        :type limit_num_rests: int
        :param print_progress: Если True - пишет прогресс выполнения
        :type print_progress: bool
        :param print_cut: Если True, то будут расписываться все распилы
        :type print_cut: bool
        :return: Зависимости в виде словаря словарей. Ключи во внешнем словаре - название класса с алгоритмом,
        значения - словари с зависимостями
        """
        result_dependence: dict[str, dict[int, float]] = dict()

        for algorithm in self.__algorithms:
            result_dependence[algorithm.__name__] = dict()

        for number_products in range(1, self.__max_num_products + 1):
            if print_progress:
                print(f'{number_products} / {self.__max_num_products}')

            for _ in range(self.__number_tests):
                # Сгенерируем случайные продукты и остатки
                products: list[float] = [round(random.uniform(min_remnant_length, whole_profile_length), 3)
                                         for _ in range(number_products)]
                remnants: list[float] = [round(random.uniform(min_remnant_length, whole_profile_length), 3)
                                         for _ in range(random.randint(0, limit_num_rests))]
                # Добавим в остатки целые профиля, чтобы точно все изделия были посчитаны
                remnants.extend([whole_profile_length for _ in range(number_products)])

                # Посчитаем для этих данных раскрои и проценты отхода
                wastes: list[tuple[str, float]] = self.test_all_algorithms(products=products,
                                                                           remnants=remnants,
                                                                           print_cut=print_cut)
                # Добавим их в итоговый словарь
                for waste in wastes:
                    # waste[0] - имя алгоритма, waste[1] - процент отхода
                    result_dependence[waste[0]][number_products] = waste[1]

        return result_dependence

    @classmethod
    def draw_graphs(cls, graphs: dict[str, dict[int, float]], file_name: str) -> None:
        """
        Функция рисует графики на одном рисунке
        :param graphs: Словарь с зависимостями. Ключи - названия графиков
        :type graphs: dict[str, dict[int, float]]
        :param file_name: Имя файла, в котором будет сохранено изображение
        :type file_name: str
        :return: None
        """
        colors: list[str] = ['red', 'green', 'blue', 'black']

        for graph, color in zip(graphs, colors):
            plt.plot(list(graphs[graph].keys()), list(graphs[graph].values()), label=graph, color=color)

        plt.xlabel('Количество изделий, шт')
        plt.ylabel('Средний процент отхода, %')
        plt.title('Сравнение зависимостей среднего процента отхода\nот количества изделий в разных алгоритмах')
        plt.legend()
        figure = plt.gcf()
        plt.show()
        figure.savefig(file_name)

    def draw_graphs_from_file(self, input_file: str, output_file: str, check_split: bool = False) -> None:
        """
        Метод берет данные из input_file, рисует график и сохраняет рисунок в utput_file
        :param input_file: Имя файла с зависимостями
        :type input_file: str
        :param output_file: Имя файла, под которым будет сохранен нарисованный график
        :type output_file: str
        :param check_split: Если True, то будет печатать разбиение строк из input_file для проверки
        :return: None
        """
        graphs: dict[str, dict[int, float]] = dict()

        with open(input_file, 'r', encoding='utf-8') as in_file:
            # Первая строка - имена алгоритмов через табуляцию
            first_line: str = in_file.readline()
            names: list[str] = first_line.rstrip().split('\t')
            if check_split:
                print('Строка из файла:', first_line)
                print('Строка после split-ов:', names)

            # Добавим пустые словари по ключам именам
            for name in names:
                graphs[name] = dict()

            # Добавим данные из файла
            for line in in_file:
                # Строка в файле имеет вид x: y1 | y2
                x_and_ys: list[str] = line.split(':')
                x: int = int(x_and_ys[0])
                ys: str = x_and_ys[1].rstrip().lstrip()
                data_str: list[str] = ys.split(' | ')
                data_float: list[float] = [float(data) for data in data_str]

                if check_split:
                    print('Строка из файла:', line)
                    print('Строка после split-ов:', x, data_float)

                for name, data in zip(names, data_float):
                    graphs[name][x] = data

        # Нарисуем графики
        self.draw_graphs(graphs, output_file)


if __name__ == '__main__':
    max_num_products: int = 60
    test_all_algorithms: TestAllAlgorithm = TestAllAlgorithm(
        algorithms=[QuickCutting, MiddleCutting],
        test_cls=TestAlgorithm,
        max_num_products=max_num_products,
        number_tests=100
    )

    difference_algorithms: dict[str, dict[int, float]] = test_all_algorithms.dependence_different_algorithms(
        print_progress=True,
        print_cut=False
    )

    test_all_algorithms.draw_graphs(difference_algorithms, 'difference_between_algorithms.jpg')

    with open('quick_middle_dependence.txt', 'w', encoding='utf-8') as file:
        print(QuickCutting.__name__, '\t', MiddleCutting.__name__)
        file.write(f'{QuickCutting.__name__}\t{MiddleCutting.__name__}\n')

        for num in range(1, max_num_products + 1):
            print('{num}: {quick_cut} | {middle_cut}'.format(
                num=num,
                quick_cut=difference_algorithms[QuickCutting.__name__][num],
                middle_cut=difference_algorithms[MiddleCutting.__name__][num]
            ))
            file.write('{num}: {quick_cut} | {middle_cut}\n'.format(
                num=num,
                quick_cut=difference_algorithms[QuickCutting.__name__][num],
                middle_cut=difference_algorithms[MiddleCutting.__name__][num]
            ))
