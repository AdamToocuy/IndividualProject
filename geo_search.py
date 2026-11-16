import os
from dotenv import dotenv_values
from dadata import Dadata

base_dir = os.path.dirname(os.path.abspath(__file__))
config = dotenv_values(os.path.join(base_dir, '.env'))
DADATA_TOKEN = config.get('DADATA_TOKEN') or os.environ.get('DADATA_TOKEN')

dadata = Dadata(DADATA_TOKEN) if DADATA_TOKEN else None


def search_address_suggestions(query: str, region: str = '', city: str = '', count: int = 10) -> list:
    if not dadata:
        print("ОШИБКА: DADATA_TOKEN не найден в .env!")
        return []

    if len(query.strip()) < 2:
        return []

    search_query = f"{city.strip()}, {query.strip()}" if city.strip() else query.strip()

    try:
        raw_results = dadata.suggest(name='address', query=search_query, count=count)
        seen_streets = set()
        suggestions = []

        for item in raw_results:
            d = item.get('data', {})
            street = d.get('street_with_type') or ''

            if street and street not in seen_streets:
                seen_streets.add(street)
                suggestions.append({
                    'value': street,
                    'text': street,
                    'district': d.get('city_district') or d.get('area') or 'unknown',
                    'lat': d.get('geo_lat') or '',
                    'lon': d.get('geo_lon') or ''
                })

        return suggestions
    except Exception as e:
        print("ОШИБКА DADATA:", e)
        return []
