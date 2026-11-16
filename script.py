import os
from dotenv import load_dotenv, dotenv_values

base_dir = os.path.dirname(os.path.abspath(__file__))
print("1. Папка скрипта:", base_dir)
print("2. Файлы в этой папке:", os.listdir(base_dir))

env_path = os.path.join(base_dir, '.env')
print("3. Файл .env найден:", os.path.exists(env_path))

# Смотрим, какие именно ключи (имена переменных) видит библиотека внутри .env
parsed = dotenv_values(env_path)
print("4. Имена переменных внутри .env:", list(parsed.keys()))

load_dotenv(dotenv_path=env_path)
print("5. Результат os.getenv('DADATA_TOKEN'):", bool(os.getenv('DADATA_TOKEN')))
