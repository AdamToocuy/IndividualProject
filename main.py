import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Маршрут для раздачи стилей из node_modules в корне проекта
@app.route('/node_modules/<path:filename>')
def node_modules(filename):
    return send_from_directory(os.path.join(app.root_path, 'node_modules'), filename)

@app.route('/')
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
