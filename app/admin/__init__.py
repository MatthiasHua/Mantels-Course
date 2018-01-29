from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
from app.modules.mark import *
import json
#创建应用实例
admin = Blueprint('admin', __name__,  template_folder='templates')

leftbarlist = (("judge_admin", "判题测试(单份)"),\
                ("judge_admin_m", "判题测试(Homework下所有)"),\
                ("access_token", "access_token"))


@admin.route('/', methods=['POST', 'GET'])
@admin.route('/judge_admin', methods=['POST', 'GET'])
def judge_admin():
    return render_template("Judge_Admin.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    leftbar = leftbarlist,\
    active = 0)

@admin.route('/judge_admin_m', methods=['POST', 'GET'])
def judge_admin_m():
    return render_template("Judge_Admin_M.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    leftbar = leftbarlist,\
    active = 1)

@admin.route('/access_token', methods=['POST', 'GET'])
def access_token():
    return render_template("Access_Token.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    leftbar = leftbarlist,\
    active = 1)


#这个函数的名词真的是。。
#按照Answer_Student中的id进行判题
@admin.route('/judgebyanswerstudentid', methods=['POST'])
def judgebyanswerstudentid():
    if request.form.get('id', '') != '':
        id = request.form.get('id', '')
        j = judge_homework_by_answer_student_id(id)
        if j > 0:
            return 'Done'
        if j == -1:
            return 'not_found'
    return '233'

#返回一个json的学生名单
#在某一课程完成某一作业作业的学生名单
#post一个作业id
@admin.route('/answer_studentid_list', methods=['POST'])
def answer_studentid_list():
    if request.form.get('id', '') != '':
        answer_student = Answer_Student.query.filter_by(homework_id = request.form.get('id', '')).all()
        answer_student_list = []
        for i in answer_student:
            answer_student_list.append(i.id)
        print(json.dumps(answer_student_list))
        return json.dumps(answer_student_list)
    return '233'
