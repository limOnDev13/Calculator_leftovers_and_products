"""
Модуль со словарем соответствий на русском
"""
BUTTONS: dict[str, str] = {
    'fabric_cutting': 'Раскрой',
    'profile_cutting': 'Распил',
    'total_cutting': 'Раскрой и распил',
    'quick_calc': 'Быстрый расчет',
    'middle_calc': 'Точный расчет',
    'reset': 'Сбросить',
    'save': 'Сохранить'
}

FRAMES: dict[str, str] = {
    'simple_cut': 'Распил'
}

LABELS: dict[str, str] = {
    'input_products': 'Введите ширины изделий (как указано в наряде):',
    'input_remnants': 'Введите ширины имеющихся остатков:',
    'input_correction': 'Введите поправку к ширине изделий:',
    'input_min_remnant': 'Введите минимальную длину остатка (м):',
    'input_whole_profile': 'Введите длину целого профиля (м):',
    'input_number_profiles': 'Введите количество целых профилей в наличии (шт):',
    'input_cutting_width': 'Введите ширину реза (м):',
    'text_result': 'Схема распила:',
    'total_waste': 'Суммарный отход (м):',
    'percent_waste': 'Процент отхода (%):'
}

ERROR_LABELS: dict[str, str] = {
    'error_input': 'Ошибка ввода параметра: ',
    'min_remnant': 'Минимальная длина остатка',
    'correction': 'Поправка к ширине изделия',
    'whole_profile': 'Длина целого профиля',
    'number_whole_profiles': 'Количество целых профилей должно быть целым числом!',
    'cut_width': 'Ширина реза',
    'float_error': 'Параметр должен быть вещественным числом (числом с плавающей точкой)!',
    'products': 'Ошибка ввода списка ширин ИЗДЕЛИЙ',
    'remnants': 'Ошибка ввода списка ширин ОСТАТКОВ'
}
