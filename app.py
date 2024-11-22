from flask import Flask, request, make_response, render_template, redirect, url_for

app = Flask(__name__, template_folder='templates')


# simple route
@app.route('/hello')
def hello():
    return 'hello people!\n'


# pass string variable
@app.route('/greet/<string:name>')
def greet(name):
    return f'Hello {name}'


# send response status code
@app.route('/hello1')
def hello1():
    response = make_response('Hello People!\n')
    response.status_code = 202
    response.headers['content-type'] = 'text/plain'
    return response


# get , post methods
@app.route('/req', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return "you made a get request\n"
    elif request.method == 'POST':
        return 'you made a post request\n'
    else:
        return 'you will never see this message.\n'


# pass int variable
@app.route('/add/<int:num1>/<int:num2>')
def add(num1, num2):
    return f'{num1} + {num2} = {num1 + num2}'


# handle url parameters
@app.route('/handle_url_params')
def handle_url_params():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args.get('greeting')
        name = request.args.get('name')
        return f'{greeting}, {name}'
    else:
        return 'Some parameters are missing.'


# templating
@app.route('/template')
def templating():
    li = ['1', '2', '3', '4']
    li1 = ['10', '20', '30', '40']
    return render_template('index.html', li=li, li1=li1)


# about page
@app.route('/filters')
def filters():
    text1 = 'Hello People'
    return render_template('filters.html', text1=text1)


# custom reverse filter
@app.template_filter("reverse_string")
def reverse_string(s):
    return s[::-1]


# custom repeat filter
@app.template_filter('repeat')
def repeat(s, times=2):
    return s * times


# custom alternatestring filter
@app.template_filter('alternatestring')
def alternatestring(s):
    return ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s)])


# redirect endpoint
@app.route('/redirect_endpoint')
def redirect_endpoint():
    return redirect(url_for('filters'))


# forms
@app.route('/form', methods=['GET', 'POST'])
def forms():
    if request.method == 'GET':
        return render_template('forms.html')
    elif request.method == 'POST':
        user = request.form['username']
        passwd = request.form['password']

        if user == 'patkar' and passwd == 'pd':
            return 'yoooo'
        else:
            return 'booooooo'


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
