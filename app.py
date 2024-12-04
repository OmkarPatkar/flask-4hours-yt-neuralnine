import os
import uuid

import pandas as pd
from flask import Flask, request, make_response, render_template, redirect, url_for, Response, send_from_directory, \
    jsonify, session

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')


# simple route
@app.route('/')
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


# file upload
@app.route('/file_upload', methods=['POST'])
def file_upload():
    file = request.files['file']
    print("File Content-Type:", file.content_type)

    if file.content_type == 'text/plain':  # Plain text file
        content = "Content in the file is: " + file.read().decode()
        return content
    elif file.content_type == 'text/csv':  # CSV file
        try:
            # Read CSV file
            df = pd.read_csv(file)
            print("DataFrame Content:\n", df)
            return df.to_html()
        except Exception as e:
            return f"An error occurred while reading the CSV file: {str(e)}", 400
    elif file.content_type in [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel'
    ]:  # Excel file
        try:
            # Read Excel file
            df = pd.read_excel(file)
            print("DataFrame Content:\n", df)
            return df.to_html()
        except Exception as e:
            return f"An error occurred while reading the Excel file: {str(e)}", 400
    else:
        return "Unsupported file type", 400


# convert csv
@app.route('/convert_csv', methods=['POST'])
def convert_csv():
    file = request.files['file']
    print("File Content-Type:", file.content_type)

    df = pd.read_excel(file)
    response = Response(
        df.to_csv(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=result.csv'
        }
    )
    return response


# convert csv and download page
@app.route('/convert_csv_download', methods=['POST'])
def convert_csv_download():
    file = request.files['file']

    df = pd.read_excel(file)

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    filename = f'{uuid.uuid4()}.csv'
    df.to_csv(os.path.join('downloads', filename))

    return render_template('download_csv.html', filename=filename)


#  endpoint for downloading csv file
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('downloads', filename, download_name='result1.csv')


# javascript json request
@app.route('/handle_post', methods=['POST'])
def handle_post():
    greetings = request.json['greeting']
    name = request.json['name']

    with open('file.txt', 'w') as f:
        f.write(f'{greetings}, {name}')

    return jsonify({'message': 'Successfully written'})


# static files and bootstrap
@app.route('/static_files')
def static_files():
    return render_template('staticFiles.html')


# session-server side
# session data is sensitive and should not be accessed or seen by the user.

# cookies-client side
app.secret_key = 'SECRET'


@app.route('/set_get_session_page')
def set_session_page():
    return render_template('set_get_session_page.html', msg='session data setting page')


@app.route('/set_data')
def set_data():
    session['name'] = 'tand'
    session['greet'] = 'yoooooo!'
    return render_template('set_get_session_page.html', msg='session data is set.')


@app.route('/get_data')
def get_data():
    if 'name' in session.keys() and 'greet' in session.keys():
        name = session['name']
        greet = session['greet']
        return render_template('set_get_session_page.html', msg=f'name: {name}, greet: {greet}')
    else:
        return render_template('set_get_session_page.html', msg=f'No session data found.')


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
