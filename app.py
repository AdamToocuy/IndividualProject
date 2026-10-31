import os
import json
import pandas as pd
from catboost import CatBoostRegressor

BASE_DIR = '/home/honor/Desktop/Индивидуальный проект'
MODEL_PATH = os.path.join(BASE_DIR, 'catboost_real_estate_model.cbm')
DICT_PATH = os.path.join(BASE_DIR, 'city_prices.json')

if not os.path.exists(MODEL_PATH) or not os.path.exists(DICT_PATH):
    print("Ошибка: Компоненты ИИ не найдены! Сначала запусти ml.py.")
    exit()

print("Загрузка искусственного интеллекта... Подождите.")
model = CatBoostRegressor()
model.load_model(MODEL_PATH)

with open(DICT_PATH, 'r', encoding='utf-8') as f:
    city_mean_price = json.load(f)

print("\n" + "="*60)
print("  ПРОФЕССИОНАЛЬНАЯ СИСТЕМА ОЦЕНКИ НЕДВИЖИМОСТИ (ИИ)  ")
print("="*60)

# Справочники кодов
purposes = {
    "1": "Жилое помещение (Квартира / Комната)",
    "2": "Нежилое помещение (Коммерция / Офис)",
    "3": "Здание / Жилой дом",
    "4": "Помещение общего пользования",
    "5": "Гараж / Машиноместо"
}
wall_materials = {
    "1": "Кирпич (Каменный)",
    "2": "Панельный дом",
    "3": "Монолитный дом",
    "4": "Блочный / Шлакоблочный",
    "5": "Деревянный / Брус"
}
realestate_types = {
    "1": "Вторичное жилье (Готовый фонд)",
    "2": "Новостройка (Строящийся фонд / ДДУ)",
    "3": "Загородная недвижимость"
}

# Ввод текстовых данных
city = input("1. Введите город (например, Москва): ").strip()
region_code_raw = input("2. Введите автомобильный код региона (например, 77): ").strip()
district = input("3. Введите административный район/округ: ").strip()
street = input("4. Введите улицу/проспект/квартал: ").strip()

print("\n--- 5. Выберите назначение объекта ---")
for num, text in purposes.items():
    print(f" [{num}] {text}")
purpose_code = input("Введите номер варианта: ").strip()

print("\n--- 6. Выберите материал стен ---")
for num, text in wall_materials.items():
    print(f" [{num}] {text}")
wall_material_code = input("Введите номер варианта: ").strip()

print("\n--- 7. Выберите тип недвижимости ---")
for num, text in realestate_types.items():
    print(f" [{num}] {text}")
realestate_type_code = input("Введите номер варианта: ").strip()

print("\n----------------------------------------------------")
doc_type = input("8. Тип документа сделки (например, Договор купли-продажи): ").strip()

try:
    area = float(input("9. Введите точную площадь объекта (кв.м.): "))
    floor = float(input("10. Введите этаж расположения: "))
    year_build = float(input("11. Введите год постройки здания: "))
    rooms = float(input("12. Введите количество комнат: ")) 
except ValueError:
    print("\n[Ошибка] Площадь, этаж, год и комнаты должны быть только числами!")
    exit()

# --- УМНАЯ ОЧИСТКА ВВОДА ДЛЯ УВЕЛИЧЕНИЯ ТОЧНОСТИ ---
city_clean = city.strip().lower()
street_clean = street.lower().replace('№', '').replace('.', '').replace(',', '').strip()
street_clean = " ".join(street_clean.split()) # удаление двойных пробелов

house_age = 2026 - year_build

# Защита от занижения цен в Москве из-за регистра ввода букв
city_mean_price_lowercase = {k.lower().strip(): v for k, v in city_mean_price.items()}
if city_clean in city_mean_price_lowercase:
    city_avg_meter_price = city_mean_price_lowercase[city_clean]
else:
    if region_code_raw == '77' or city_clean == 'москва':
        city_avg_meter_price = 320000.0  # Средняя цена метра в Москве
    else:
        city_avg_meter_price = 135000.0  # Базовая цена для неизвестных регионов

# Создание DataFrame со СТРОГИМ порядком колонок из ml.py
user_data = pd.DataFrame([{
    'area': area,
    'floor': floor,
    'year_build': year_build,
    'region_code': float(region_code_raw) if region_code_raw.isdigit() else 77.0,
    'number': rooms,
    'house_age': house_age,
    'city_avg_meter_price': city_avg_meter_price,
    'city': str(city_clean),
    'street': str(street_clean),
    'district': str(district).strip().lower(),
    'wall_material_code': str(wall_material_code),
    'realestate_type_code': str(realestate_type_code),
    'purpose_code': str(purpose_code),
    'doc_type': str(doc_type).strip().lower()
}])

feature_order = [
    'area', 'floor', 'year_build', 'region_code', 'number', 'house_age', 'city_avg_meter_price',
    'city', 'street', 'district', 'wall_material_code', 'realestate_type_code', 'purpose_code', 'doc_type'
]
user_data = user_data[feature_order]

# Расчет цены
predicted_price = model.predict(user_data)[0]

if predicted_price < 0:
    predicted_price = city_avg_meter_price * area

print("\n" + "="*60)
print(f" РЕЗУЛЬТАТ СТОИМОСТНОЙ ЭКСПЕРТИЗЫ ИИ:")
print(f" Рекомендуемая рыночная стоимость: {predicted_price:,.2f} руб.")
print(f" Базовая стоимость кв. метра в локации: {city_avg_meter_price:,.2f} руб./кв.м.")
print("="*60)
