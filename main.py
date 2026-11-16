import os
import json
from flask import Flask, render_template, send_from_directory, request, jsonify
from geo_search import search_address_suggestions

app = Flask(__name__)

JSON_PATH = os.path.join(app.root_path, 'data.json')
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    REGION_TO_CITIES = json.load(f)

REGIONS = list(REGION_TO_CITIES.keys())


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/suggest-address', methods=['GET', 'POST'])
def suggest_address():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        query = data.get('query', '')
        region = data.get('region', '')
        city = data.get('city', '')
    else:
        query = request.args.get('q', '')
        region = request.args.get('region', '')
        city = request.args.get('city', '')

    suggestions = search_address_suggestions(query=query, region=region, city=city)
    return jsonify(suggestions)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    selected_region = request.args.get('region', '')
    selected_city = request.args.get('city', '')
    cities = REGION_TO_CITIES.get(selected_region, [])
    user_input = None

    if request.method == 'POST':
        user_input = request.form.to_dict()
        selected_region = user_input.get('region', '')
        selected_city = user_input.get('city', '')
        cities = REGION_TO_CITIES.get(selected_region, [])

    return render_template(
        'predict.html',
        regions=REGIONS,
        cities=cities,
        selected_region=selected_region,
        selected_city=selected_city,
        user_input=user_input
    )


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/node_modules/<path:filename>')
def node_modules(filename):
    return send_from_directory(os.path.join(app.root_path, 'node_modules'), filename)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
