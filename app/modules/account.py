#账户相关库
from flask import session, request
from app import db
from app.model import *
from app.modules import checkform

#---------------------------------------
#教师登录
#输入:
#number 账号
#password 密码
#输出:
#int: result       为1时登录成功，为-1时用户名和密码不匹配
#---------------------------------------
def teacher_sign_in(form):
    teacher = Teacher.query.filter_by(number = form['number']).first()
    if teacher != None and teacher.password == form['password']:
        session['username'] = teacher.username
        session['signin'] = True
        session['id'] = teacher.id
        session['role'] = 'Teacher'
        if teacher.role == 9:
            session['admin'] = 9
        return 1
    else:
        return -1

#---------------------------------------
#教师注册
#输入:
#number 账号
#username 用户名
#password 密码
#输出:
#int: result       为1时注册成功，为-1账号已被注册
#---------------------------------------
def teacher_register(form):
    #检查账号重复,账号已被注册返回-1
    teacher = Teacher.query.filter_by(number = form['number']).first()
    if teacher != None:
        return -1
    teacher = Teacher.query.filter_by(email = form['email']).first()
    if teacher != None:
        return -2
    if checkform.new_teacher(form) == 1:
        newTeacher = Teacher(request.form['number'], request.form['username'], request.form['email'], request.form['password'], 1, -1)
        db.session.add(newTeacher)
        db.session.commit()
        return 1
    else:
        return checkform.new_teacher(form) - 10

#---------------------------------------
#学生登录
#输入:
#number 账号
#password 密码
#输出:
#int: result       为1时登录成功，为-1时用户名和密码不匹配
#---------------------------------------
def student_sign_in(form):
    student = Student.query.filter_by(number = request.form['number']).first()
    if student != None and student.password == form['password']:
        session['username'] = student.username
        session['signin'] = True
        session['id'] = student.id
        session['role'] = 'Student'
        return 1
    else:
        return -1

#---------------------------------------
#学生登录(第三方设备)
#输入:
#number 账号
#password 密码
#输出:
#int: result       为1时登录成功
#---------------------------------------
def student_key_sign_in(form, student_key):
    studentkey = Student_Key.query.filter_by(content = student_key).first()
    student = Student.query.filter_by(number = request.form['number']).first()
    #验证账号密码
    if student != None and student.password == form['password']:
        #删除旧的登录记录
        oldstudentkey = Student_Key.query.filter_by(student_id = student.id).all()
        for i in oldstudentkey:
            db.session.delete(i)
        db.session.commit()
        #启用当前student_key
        studentkey.student_id = student.id
        studentkey.enable = 'True'
        db.session.commit()
        return 1
    else:
        return -1

#---------------------------------------
#学生注册
#输入:
#number 账号
#username 用户名
#password 密码
#输出:
#int: result       为1时注册成功，为-1账号已被注册
#---------------------------------------
def student_register(form):
    #检查账号重复,账号已被注册返回-1
    student = Student.query.filter_by(number = form['number']).first()
    if student != None:
        return -1
    #检查邮箱重复,邮箱已被注册返回-2
    student = Student.query.filter_by(email = form['email']).first()
    if student != None:
        return -2
    if checkform.new_student(form) == 1:
        newStudent = Student(request.form['number'], request.form['username'], request.form['email'], request.form['password'])
        db.session.add(newStudent)
        db.session.commit()
        return 1
    else:
        #返回错误编号
        return checkform.new_student(form) - 10
