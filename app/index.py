#主页

from app import app
from flask import render_template, session

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
	return render_template('index.html',\
	role = session.get('role', ''),\
	username = session.get('username', ''))

@app.route('/404', methods=['GET'])
def error_404():
	return render_template('404.html')

@app.route('/test', methods=['GET'])
def test():
	return render_template('test.html')

@app.route('/feedback', methods=['POST'])
def feedback():
	return render_template('404.html')
