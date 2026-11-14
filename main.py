import os
import json
from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)

def load_geo_data():
    json_path = os.path.join(app.root_path, 'data.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    region_to_cities = {}
    for item in raw_data:
        reg = item.get("region")
        city = item.get("city")
        if reg and city:
            region_to_cities.setdefault(reg.strip(), []).append(city.strip())
            
    regions = sorted(region_to_cities.keys())
    for reg in region_to_cities:
        region_to_cities[reg] = sorted(list(set(region_to_cities[reg])))
        
    return regions, region_to_cities

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    regions, region_to_cities = load_geo_data()
    
    if request.method == 'POST':
        user_input = request.form.to_dict()
        print("Полученные данные:", user_input)
        
    return render_template(
        'predict.html',
        regions=regions,
        region_to_cities=region_to_cities
    )

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/node_modules/<path:filename>')
def node_modules(filename):
    return send_from_directory(os.path.join(app.root_path, 'node_modules'), filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
