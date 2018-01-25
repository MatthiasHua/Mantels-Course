from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
from app.modules.coursemanager import *

#创建应用实例
teacher = Blueprint('teacher', __name__,  template_folder='templates')

leftbarlist = (("mycourses", "我的课程"),\
               ("newcourse", "创建课程"),\
               ("schedule", "课程表"))

#主页
@teacher.route('/', methods=['POST', 'GET'])
@teacher.route('/index', methods=['POST', 'GET'])
@teacher.route('/mycourses', methods=['POST', 'GET'])
def mycourses():
    user = Teacher.query.filter_by(username = session['username']).first()
    allclasses = user.classpost.all()
    return render_template("MyCourses.html",\
	role = session.get('role', ''),\
	username = session.get('username', ''),\
    leftbar = leftbarlist,\
    active = 0,\
    allclasses = allclasses)

@teacher.route('/newcourse', methods=['POST', 'GET'])
def newcourse():
    if request.method == 'GET':
        return render_template("NewCourse.html",\
    	role = session.get('role', ''),\
    	username = session.get('username', ''),\
        leftbar = leftbarlist,\
        active = 1)
    if request.method == 'POST':
        #从POST请求中获取表单
        newclassform = request.form.to_dict()
        #加入用户id
        newclassform['id'] = session['id']
        #创建课程
        print(newclassform)
        if new_course_form(newclassform) == 1:
            return 'Done'
        else:
            #创建课程失败
            return "233"

@teacher.route('/schedule', methods=['POST', 'GET'])
def schedule():
    return render_template("Schedule.html",\
	role = session.get('role', ''),\
	username = session.get('username', ''),\
    leftbar = leftbarlist,\
    active = 2)

#需要对表单进行验证
#现在只简单确认表单不为空
def checkform_newcourse(form):
    if form['coursename'] == '':
        return False
    if form['courseid'] == '':
        return False
    if form['start'] == '':
        return False
    if form['end'] == '':
        return False
    if form['introduction'] == '':
        return False
    return True
