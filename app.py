from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'hello people!\n'


@app.route('/greet/<string:name>')
def greet(name):
    return f'Hello {name}'


@app.route('/hello1')
def hello1():
    response = make_response('Hello People!\n')
    response.status_code = 202
    response.headers['content-type'] = 'text/plain'
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return "you made a get request\n"
    elif request.method == 'POST':
        return 'you made a post request\n'
    else:
        return 'you will never see this message.\n'


@app.route('/add/<int:num1>/<int:num2>')
def add(num1, num2):
    return f'{num1} + {num2} = {num1 + num2}'


@app.route('/handle_url_params')
def handle_url_params():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args.get('greeting')
        name = request.args.get('name')
        return f'{greeting}, {name}'
    else:
        return 'Some parameters are missing.'


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
