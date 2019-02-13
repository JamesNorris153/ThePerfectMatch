from flask import Flask, render_template, request
from flask_cors import CORS
from models import authenticate
#Example for importing methods
#from models import get_users, create_user, get_user

app = Flask(__name__, static_url_path='/static')

CORS(app)

## Sends static files when necessary
@app.route('/static/<path:path>')
def send_js(path):
	return send_from_directory('static',path)

## Landing page
@app.route('/', methods=['GET', 'POST'])
def index():

	if request.method == "GET":
		return render_template('index.html')

	if request.method == "GET":
		username = request.form.get('username')
		password = request.form.get('password')
		if authenticate(username, password):
			return 'Template not yet implemented'
		else:
			return render_template('index.html', error = "Incorrect username or password")

@app.route('/', methods=['POST'])

## Internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")

## Page not found
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True)
