from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
#创建应用实例
about = Blueprint('about', __name__,  template_folder='templates')


#主页
@about.route('/', methods=['POST', 'GET'])
@about.route('/index', methods=['POST', 'GET'])
def aboutindex():
    return render_template("AboutIndex.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''))
