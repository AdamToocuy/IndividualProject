from flask import Flask, render_template

app = Flask(__name__)

<<<<<<< HEAD
@app.route('/')
def home():
    # Вызываем дочерний шаблон index.html, 
    # который автоматически подтянет и соберет base.html
    return render_template('index.html')
=======
# Исправленный маршрут с параметром пути
@app.route('/node_modules/<path:filename>')
def node_modules(filename):
    return send_from_directory(os.path.join(app.root_path, 'node_modules'), filename)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')
>>>>>>> e314c37 (Добавление функционала у кнопок, удаление лишнего)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
