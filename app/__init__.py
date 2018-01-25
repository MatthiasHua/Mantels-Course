import configparser
#日志
from app.logging import logging
#网络框架
from flask import Flask, session, render_template, request, redirect, url_for
#orm
from flask_sqlalchemy import SQLAlchemy

#设置文件
config = configparser.ConfigParser()
#读入设置
config.read("config.ini")

#建立网站实例
app = Flask(__name__)
#载入设置
app.config.from_object('config')

########
#数据库#
########
db = SQLAlchemy(app)
from app.model import *

#登陆检查
@app.before_request
def check_need_login():
	allowlist = ('index', 'user_base.signin', 'user_base.register',\
	'courses.coursesindex', 'user_base.studentsignin', 'user_base.studentregister')
	forbidstudent = ('teacher', 'editcourses')
	print(request.endpoint)
	#学生限制访问
	if session.get('role', '') == 'Student':
		#禁止访问教师后台
		if request.endpoint.startswith('teacher'):
			return redirect(url_for('courses.coursesindex'))
	if not session.get('signin', False)  and request.endpoint not in allowlist:
		return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html',\
	role = session.get('role', ''),\
	username = session.get('username', ''))

def importmodule(bp):
    logging.info(" * Import module:" + bp[0])
	#import模块
    bpmodule = __import__("app." + bp[0], globals(), locals(), list(bp[0]))
    #获取应用实例
    bpapp = getattr(bpmodule, bp[0])
    #通过蓝图挂载应用实例
    app.register_blueprint(bpapp, url_prefix = "/" + bp[0])

#载入Base中的框架
list(map(importmodule, list(i for i in config.items("Base") if i[1] == "True")))
