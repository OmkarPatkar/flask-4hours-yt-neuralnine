from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "yooooo"


@app.route('/greet/<string:name>')
def greet(name):
    return f'Hello {name}'


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
