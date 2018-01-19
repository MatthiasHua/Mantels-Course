from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
#创建应用实例
student = Blueprint('student', __name__,  template_folder='templates')

leftbarlist = (("studentindex", "课程中心"),\
               ("courseselection", "选课"),\
               ("schedule_student", "课程表"))

#课程中心
@student.route('/', methods=['POST', 'GET'])
@student.route('/studentindex', methods=['POST', 'GET'])
def studentindex():
    return render_template("StudentCourseCenter.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    leftbar = leftbarlist,\
    active = 0)

#选课
@student.route('/courseselection', methods=['POST', 'GET'])
def courseselection():
    student = Student.query.filter_by(username = session['username']).first()
    ic = student.involed_class.all()
    if request.method == 'GET':
        allclasses = Class.query.all()
        involedclasses = []
        for i in ic:
            involedclasses.append(i.id)
        return render_template("Courseselection.html",\
        allclasses = allclasses,\
        involedclasses = involedclasses,\
        role = session.get('role', 'unknow'),\
        username = session.get('username', ''),\
        leftbar = leftbarlist,\
        active = 1)
    else:
        print(request.form)
        for i in ic:
            if i.class_id == request.form.get('id', ''):
                return 'alreadyinvoled'
        if request.form.get('course', '') == 'select' and request.form.get('id', '') != '':
            newinvoledclass = Involed_class(request.form.get('id'), session['id'])
            db.session.add(newinvoledclass)
            db.session.commit()
            return 'Done'
        if request.form.get('course', '') == 'quit' and request.form.get('id', '') != '':
            check = Involed_class.query.filter_by(student_id = session['id'], class_id = request.form.get('id')).first()
            if check == None:
                return 'notinvoled'
            else:
                db.session.delete(check)
                db.session.commit()
                return 'Done'
        return '233'

#课程表
@student.route('/schedule_student', methods=['POST', 'GET'])
def schedule_student():
    return render_template("Schedule_student.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    leftbar = leftbarlist,\
    active = 2)
