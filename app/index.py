#主页

from app import app
from flask import render_template, session

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html',\
	role = session.get('role', ''),\
	username = session.get('username', ''))
