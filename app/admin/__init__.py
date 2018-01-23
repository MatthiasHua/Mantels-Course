from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
import json
#创建应用实例
admin = Blueprint('admin', __name__,  template_folder='templates')

leftbarlist = (("judge_admin", "判题测试(单份)"),\
                ("judge_admin_m", "判题测试(Homework下所有)"))


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

#这个函数的名词真的是。。
#按照Answer_Student中的id进行判题
#这个函数太长了。。
@admin.route('/judgebyanswerstudentid', methods=['POST'])
def judgebyanswerstudentid():
    if request.form.get('id', '') != '':
        answer_student = Answer_Student.query.filter_by(id = request.form.get('id', '')).all()
        #没找到
        if answer_student == []:
            return 'not_found'
        #批改结果
        result = ''
        sum = 0
        #作业的id
        homework_id = answer_student[0].homework_id
        #标准答案
        answer = Answer.query.filter_by(homework_id = homework_id).first()
        #分值
        score = Score.query.filter_by(homework_id = homework_id).first()


        answer_list = answer.body.split('~')
        #学生答案
        answer_student_list = answer_student[0].body.split('~')
        score_list = score.body.split('~')

        for index, a in enumerate(answer_student_list):
            if a == answer_list[index]:
                result += score_list[index]+'~'
                sum += int(score_list[index])
            else:
                result += '0~'
        result += str(sum)
        print(result)
        old_score_student = Score_Student.query.filter_by(homework_id = homework_id, student_id = answer_student[0].student_id).all()
        if old_score_student != []:
            old_score_student[0].body = result
        else:
            score_student = Score_Student(result, answer_student[0].student_id, homework_id)
            db.session.add(score_student)
        db.session.commit()
        return 'Done'
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
