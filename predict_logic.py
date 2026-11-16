import os
from dotenv import load_dotenv


load_dotenv()

DADATA_TOKEN = os.getenv('DADATATOKEN')

print(DADATA_TOKEN[:5])