from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
#创建应用实例
markdowneditor = Blueprint('markdowneditor', __name__,  template_folder='templates')

#主页
@markdowneditor.route('/', methods=['POST', 'GET'])
@markdowneditor.route('/index', methods=['POST', 'GET'])
def editor():
    user = Teacher.query.filter_by(username = session['username']).first()
    allclasses = user.classpost.all()
    return render_template("MarkdownEditor.html",\
	role = session.get('role', ''),\
	username = session.get('username', ''),\
    active = 0)

@markdowneditor.route('/guide', methods=['POST', 'GET'])
def markdownguide():
    user = Teacher.query.filter_by(username = session['username']).first()
    allclasses = user.classpost.all()
    return render_template("MarkdownGuide.html",\
	role = session.get('role', ''),\
	username = session.get('username', ''),\
    active = 0)
