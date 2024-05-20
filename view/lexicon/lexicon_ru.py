"""
Модуль со словарем соответствий на русском
"""
BUTTONS: dict[str, str] = {
    'fabric_cutting': 'Раскрой',
    'profile_cutting': 'Распил',
    'total_cutting': 'Раскрой и распил',
    'quick_calc': 'Быстрый расчет',
    'middle_calc': 'Точный расчет',
    'reset': 'Сбросить'
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
    'input_cutting_width': 'Введите ширину реза (м):'
}
