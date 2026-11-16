import os
from dotenv import dotenv_values
from dadata import Dadata


base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '.env')

# Читаем .env напрямую в словарь
config = dotenv_values(env_path)
DADATA_TOKEN = config.get('DADATA_TOKEN')


dadata = Dadata(DADATA_TOKEN)
result = dadata.suggest("address", "Ростов-на-Дону")
address = dadata.suggest(locations=[{"region_with_type": "Ростовская область", "city": "Ростов-на-Дону"}], name='address', query='ул. теа')

for item in address:
    print(item['data'].get('street_with_type'))
