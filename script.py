import json
import geonamescache

def normalize(name):
    return name.strip().lower().replace("ё", "е")

def main():
    print("Загружаю локальный офлайн-справочник населённых пунктов...")
    gc = geonamescache.GeonamesCache()
    cities_db = gc.get_cities()

    # Собираем все действующие населённые пункты России с населением >= 1000
    valid_ru_places = set()
    for city_info in cities_db.values():
        if city_info.get("countrycode") == "RU" and city_info.get("population", 0) >= 1000:
            # Добавляем основное название и все русские альтернативные названия
            valid_ru_places.add(normalize(city_info.get("name", "")))
            for alt in city_info.get("alternatenames", []):
                # Берём кириллические названия
                if any("а" <= ch <= "я" or ch == "ё" for ch in alt.lower()):
                    valid_ru_places.add(normalize(alt))

    print(f"В офлайн-базе найдено действующих НП РФ (население >= 1000): {len(valid_ru_places)}")

    with open("data.json", "r", encoding="utf-8") as f:
        my_data = json.load(f)

    initial_count = len(my_data)
    cleaned_data = []
    seen = set()

    for item in my_data:
        reg = item.get("region", "").strip()
        city = item.get("city", "").strip()

        if not reg or not city:
            continue

        # Проверяем наличие в актуальном справочнике с населением >= 1000
        if normalize(city) in valid_ru_places:
            pair = (reg, city)
            if pair not in seen:
                seen.add(pair)
                cleaned_data.append({"region": reg, "city": city})

    # Перезаписываем data.json
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"Готово! Файл data.json перезаписан за 0.1 сек.")
    print(f"Было записей: {initial_count} -> Стало: {len(cleaned_data)} (удалено {initial_count - len(cleaned_data)}).")

if __name__ == "__main__":
    main()