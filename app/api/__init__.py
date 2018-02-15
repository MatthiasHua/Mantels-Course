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
    device_name = data.get('device name')
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
    if verificate(number + token + device_name) == verification_code:
        accesskey = create_key(16)
        try:
            newaccesskey = Access_Key.query.filter_by(teacher_id = teacher[0].id, device_name = device_name).all()
            if newaccesskey == []:
                print(int(time.time()))
                newaccesskey = Access_Key(teacher[0].id, device_name, accesskey, int(time.time()), int(time.time()) + lasttime, 'none')
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

@api.route('/experiment/new_result', methods=['POST', 'GET'])
def cexperiment_new_result():
    data = request.get_data('content').decode('utf8')
    data = json.loads(data)
    index = data.get('index')
    access_key = data.get('access_key')
    device_name = data.get('device_name')
    experiment_id = data.get('experiment_id')
    class_id = data.get('class_id')
    student_id = data.get('student_id')
    content = data.get('content')
    time = data.get('time')
    verification_code = data.get('verification code')
    print(index, access_key, device_name, experiment_id, class_id, student_id, content, time)
    if verificate(index + access_key + device_name + experiment_id + class_id + student_id + content + time) != verification_code:
        #校验码错误
        return '40006'
    accesskey = Access_Key.query.filter_by(content = access_key, device_name = device_name).all()
    if accesskey == []:
        #错误的access_key或device_name
        return '40001'
    accesskey = accesskey[0]
    theclass = Class.query.filter_by(id = class_id).all()
    if accesskey == []:
        #不存在的课程
        return '40002'
    theclass = theclass[0]
    theexperiment = Experiment.query.filter_by(id = experiment_id)
    if accesskey == []:
        #不存在的实验
        return '40003'
    theexperiment = theexperiment[0]
    if accesskey.teacher_id != theclass.teacher_id:
        #当前教师权限不足
        return '40004'
    if theexperiment.class_id != theclass.id:
        #experiment_id错误
        return '40005'
    newexperimentresult = ExperimentResult(index, device_name, experiment_id, class_id, student_id, content, time)
    db.session.add(newexperimentresult)
    db.session.commit()
    return "success"
