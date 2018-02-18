from flask import Blueprint, render_template, redirect, url_for, request, session
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
from app.modules import account
#创建应用实例
user_base = Blueprint('user_base', __name__,  template_folder='templates', static_folder='static')

#登录
@user_base.route('/', methods=['POST', 'GET'])
@user_base.route('/index', methods=['POST', 'GET'])
@user_base.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'GET':
        #登录界面
        return render_template("Signin.html")
    if request.method == 'POST':
        #登录
        return str(account.teacher_sign_in(request.form))

#注册
@user_base.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        #注册界面
        return render_template("Register.html")
    if request.method == 'POST':
        #注册
        return str(account.teacher_register(request.form))

#注销
@user_base.route('/logout')
def logout():

    session['signin'] = False
    session['username'] = 'unknow'
    session['number'] = ''
    session['id'] = ''
    session['admin'] = '9'
    if session['role'] == 'Teacher':
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
        #登录
        return str(account.student_sign_in(request.form))

#学生注册
@user_base.route('/student/register', methods=['POST', 'GET'])
def studentregister():
    if request.method == 'GET':
        return render_template("StudentRegister.html")
    if request.method == 'POST':
        #注册
        return str(account.student_register(request.form))

#学生登录至其它设备
@user_base.route('/student_key/signin/<string:student_key>', methods=['POST', 'GET'])
def student_key_signin(student_key):
    studentkey = Student_Key.query.filter_by(content = student_key).first()
    if studentkey  == None or studentkey.enable == 'True':
        return redirect(url_for('error_404'))
    if request.method == 'GET':
        return render_template("Student_Key_Signin.html",\
        student_key = student_key)
    if request.method == 'POST':
        return str(account.student_key_sign_in(request.form, student_key))

#登录成功(仅提升成功)
@user_base.route('/success', methods=['GET'])
def signin_success():
    return render_template("sign_in_success.html")
