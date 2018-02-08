from flask import Blueprint, render_template, redirect, url_for, request, session
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
#创建应用实例
user_base = Blueprint('user_base', __name__,  template_folder='templates', static_folder='static')

#登录
@user_base.route('/', methods=['POST', 'GET'])
@user_base.route('/index', methods=['POST', 'GET'])
@user_base.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'GET':
        return render_template("Signin.html")
    if request.method == 'POST':
        teacher = Teacher.query.filter_by(number = request.form['number']).first()
        if teacher != None and teacher.password == request.form['password']:
            session['username'] = teacher.username
            session['signin'] = True
            session['id'] = teacher.id
            session['role'] = 'Teacher'
            if teacher.role == 9:
                session['admin'] = 9
            return 'Done'
        else:
            return '233'

#注册
@user_base.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("Register.html")
    if request.method == 'POST':
        if post_check(request.form):
            newTeacher = Teacher(request.form['number'], request.form['username'], request.form['email'], request.form['password'], 1, -1)
            db.session.add(newTeacher)
            db.session.commit()
            return 'Done'
        else:
            return '233'

#注销
@user_base.route('/logout')
def logout():
    session['signin'] = False
    session['username'] = 'unknow'
    session['id'] = ''
    session['admin'] = '9'
    if session['role'] == 'teacher':
        session['role'] = 'unknow'
        return redirect(url_for("index"))
    else:
        session['role'] = 'unknow'
        return redirect(url_for("courses.coursesindex"))

#学生登录
@user_base.route('/student/signin', methods=['POST', 'GET'])
def studentsignin():
    if request.method == 'GET':
        return render_template("StudentSignin.html")
    if request.method == 'POST':
        user = Student.query.filter_by(number = request.form['number']).first()
        if user != None and user.password == request.form['password']:
            session['username'] = user.username
            session['signin'] = True
            session['id'] = user.id
            session['role'] = 'Student'
            return 'Done'
        else:
            return '233'

#学生注册
@user_base.route('/student/register', methods=['POST', 'GET'])
def studentregister():
    if request.method == 'GET':
        return render_template("StudentRegister.html")
    if request.method == 'POST':
        print(request.form)
        if post_check(request.form):
            newStudent = Student(request.form['number'], request.form['username'], request.form['email'], request.form['password'])
            db.session.add(newStudent)
            db.session.commit()
            return 'Done'
        else:
            return '233'

#学生登录至其它设备
@user_base.route('/student_key/signin/<string:student_key>', methods=['POST', 'GET'])
def student_key_signin(student_key):
    studentkey = Student_Key.query.filter_by(content = student_key).all()
    if studentkey  == [] or studentkey[0].enable == 'True':
        return "404"
    if request.method == 'GET':
        return render_template("Student_Key_Signin.html",\
        student_key = student_key)
    if request.method == 'POST':
        print(233)
        user = Student.query.filter_by(number = request.form['number']).first()
        oldstudentkey = Student_Key.query.filter_by(student_id = user.id).all()
        if oldstudentkey  != []:
            db.session.delete(oldstudentkey[0])
            db.session.commit()
        studentkey[0].student_id = user.id
        studentkey[0].enable = 'True'
        db.session.commit()
        if user != None and user.password == request.form['password']:
            session['username'] = user.username
            session['signin'] = True
            session['id'] = user.id
            session['role'] = 'Student'
            return 'Done'
        else:
            return '233'



#检查用户名、邮箱、密码是否合法
def post_check(form):
    if form.get('username') == '':
        return 0
    if form.get('email') == '':
        return 0
    if form.get('password') == '':
        return 0
    return 1
