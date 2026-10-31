import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score 
from catboost import CatBoostRegressor
import json

# 1. Загрузка данных
df = pd.read_csv('real_property_deals_russia_2024-2026.csv', low_memory=False)

target_column = 'deal_price'
numerical_features = ['area', 'floor', 'year_build', 'region_code', 'number']
categorical_features = ['city', 'street', 'district', 'wall_material_code', 'realestate_type_code', 'purpose_code', 'doc_type']

# Принудительно очищаем числовые столбцы
for col in numerical_features + [target_column]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Фильтрация диких выбросов и аномалий рынка недвижимости
if 'currency' in df.columns:
    df = df[df['currency'].astype(str).str.upper().str.contains('RUB|РУБ', na=True)]
df = df[(df[target_column] >= 1_000_000) & (df[target_column] <= 150_000_000)]
df = df[(df['area'] >= 10) & (df['area'] <= 500)]
df = df[(df['number'] >= 1) & (df['number'] <= 6)]

# Нормализуем текстовые колонки для стабильного совпадения
df_clean = df[numerical_features + categorical_features + [target_column]].dropna().copy()
for col in categorical_features:
    df_clean[col] = df_clean[col].astype(str).str.strip().str.lower()
    # Очистка названий улиц от специфических символов
    if col == 'street':
        df_clean[col] = df_clean[col].str.replace('№', '').str.replace('.', '').str.replace(',', '')

# --- СОЗДАНИЕ НОВЫХ УМНЫХ ПРИЗНАКОВ (Feature Engineering) ---
df_clean['house_age'] = 2026 - df_clean['year_build']
numerical_features.append('house_age')

df_clean['price_per_meter'] = df_clean[target_column] / df_clean['area']
city_mean_price = df_clean.groupby('city')['price_per_meter'].mean().to_dict()
df_clean['city_avg_meter_price'] = df_clean['city'].map(city_mean_price)
numerical_features.append('city_avg_meter_price')

df_clean = df_clean.drop(columns=['price_per_meter'])
# ------------------------------------------------------------

final_features = numerical_features + categorical_features
X = df_clean[final_features]
y = df_clean[target_column]

print(f"Размер выборки для обучения: {X.shape[0]:,} строк.")

# 2. Разделение на train и test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Настройка и обучение CatBoost
model = CatBoostRegressor(
    iterations=1000,         
    learning_rate=0.05,      
    depth=8,                 
    cat_features=categorical_features,
    random_seed=42,
    verbose=100,             
    thread_count=-1          
)

print("\nСтарт глубокого обучения CatBoost...")
model.fit(X_train, y_train, eval_set=(X_test, y_test), use_best_model=True)

# Проверка качества
prediction = model.predict(X_test)
print(f"\nТочность на тесте (R2 Score): {r2_score(y_test, prediction):.2%}")

# 4. Выгрузка обученной модели и словаря цен в папку проекта
model_path = '/home/honor/Desktop/Индивидуальный проект/catboost_real_estate_model.cbm'
model.save_model(model_path)

dict_path = '/home/honor/Desktop/Индивидуальный проект/city_prices.json'
with open(dict_path, 'w', encoding='utf-8') as f:
    json.dump(city_mean_price, f, ensure_ascii=False, indent=4)

print("\n[УСПЕХ] Экспорт завершен! Все файлы созданы.")
