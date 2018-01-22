from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
#创建应用实例
help = Blueprint('help', __name__,  template_folder='templates')

leftbar = ['Mantels Courses 帮助手册', 'Markdown', '习题系统', '成绩系统', '&nbsp;&nbsp;缩进233']

@help.route('/', methods=['POST', 'GET'])
@help.route('/index', methods=['POST', 'GET'])
def helpindex():
    return render_template(leftbar[0]+".html",\
    leftbar = leftbar,\
    active = 0,\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''))

@help.route('/<int:id>', methods=['POST', 'GET'])
def helpbook(id):
    return render_template(leftbar[id]+".html",\
    leftbar = leftbar,\
    active = id,\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''))
