#主页

from app import app
from flask import render_template, session

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html',\
	role = session.get('role', ''),\
	username = session.get('username', ''))

@app.route('/404')
def error_404():
	return render_template('404.html')
