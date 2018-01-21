from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
#创建应用实例
homework = Blueprint('homework', __name__,  template_folder='templates')

@homework.route('/id/<int:id>', methods=['POST', 'GET'])
def homework_edit(id):
    homework = Homework.query.filter_by(id = id).first()
    print(homework)
    return render_template("Homework.html",\
    homework = homework,\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    active = 2)
