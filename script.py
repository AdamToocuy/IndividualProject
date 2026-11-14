import json


def ru_sort_key(text):
    return text.lower().replace('ё', 'е' + chr(0xFFFF))


def sort_json_alphabetically():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    sorted_data = {
        region: sorted(cities, key=ru_sort_key)
        for region, cities in sorted(data.items(), key=lambda item: ru_sort_key(item[0]))
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    sort_json_alphabetically()
