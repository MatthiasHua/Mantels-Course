from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
from app.modules.key import *
import json
import time

#创建应用实例
api = Blueprint('api', __name__,  template_folder='templates')

@api.route('/access_key', methods=['POST', 'GET'])
def access_key():
    data = request.get_data('content').decode('utf8')
    data = json.loads(data)
    number = data.get('number')
    token = data.get('token')
    lasttime = int(data.get('last time', 7200))
    if lasttime > 43200:
        return '40006'
    teacher = Teacher.query.filter_by(number = number).all()
    if teacher == []:
        return '40001'
    token_db = Token.query.filter_by(teacher_id = teacher[0].id).all()
    if token_db == []:
        return '40002'
    if token_db[0].content != token:
        print(token_db[0].content)
        print(token)
        return '40003'
    verification_code = data.get('verification code')
    print(number, token, verification_code)
    if verificate(number + token) == verification_code:
        accesskey = create_key(16)
        try:
            newaccesskey = Access_Key.query.filter_by(teacher_id = teacher[0].id).all()
            if newaccesskey == []:
                print(int(time.time()))
                newaccesskey = Access_Key(teacher[0].id, accesskey, int(time.time()), int(time.time()) + lasttime, 'none')
                db.session.add(newaccesskey)
            else:
                newaccesskey = newaccesskey[0]
                newaccesskey.content = accesskey
                newaccesskey.time = int(time.time())
                newaccesskey.last = int(time.time()) + lasttime
            db.session.commit()
        except BaseException as e:
            print(e)
            return "40004"
        verification_code = verificate(number + accesskey)
        data = {
            'access_key': accesskey,
            'verification code': verification_code
        }
        data = json.dumps(data)
        data = bytes(data, 'utf8')
        return data
    else:
        #校验码错误
        print(verificate(number + token))
        return "40005"

@api.route('/student_key', methods=['POST', 'GET'])
def student_key():
    data = request.get_data('content').decode('utf8')
    data = json.loads(data)
    access_key = data.get('access_key')
    lasttime = int(data.get('last time', 7200))
    verification_code = data.get('verification code')
    if  verificate(access_key + str(lasttime)) == verification_code:
        newkey = create_key(16)
        newStudent_Key = Student_Key(0, newkey, 'False', int(time.time()), int(time.time()) + lasttime)
        db.session.add(newStudent_Key)
        db.session.commit()
        verification_code = verificate(access_key + newkey)
        data = {
            'student_key': newkey,
            'verification code': verification_code
        }
        data = json.dumps(data)
        data = bytes(data, 'utf8')
        return data
    else:
        #校验码错误
        return "40001"

@api.route('/check_email/teacher/<string:key>', methods=['POST', 'GET'])
def check_email_teacher(key):
    find = Email_check_key_teacher.query.filter_by(key = key).all()
    if find == []:
        return "404"
    elif find[0].time < time.time():
        return "链接已失效"
    else:
        find[0].time = 0
        teacher_id = find[0].teacher_id
        teacher = Teacher.query.filter_by(id = teacher_id).first()
        teacher.email_check = 1
        db.session.commit()
        return "邮箱验证成功"
    return "404"

@api.route('/check_email/student/<string:key>', methods=['POST', 'GET'])
def check_email_student(key):
    find = Email_check_key_student.query.filter_by(key = key).all()
    if find == []:
        return "404"
    elif find[0].time < time.time():
        return "链接已失效"
    else:
        find[0].time = 0
        student_id = find[0].student_id
        student = Student.query.filter_by(id = student_id).first()
        student.email_check = 1
        db.session.commit()
        return "邮箱验证成功"
    return "404"
