from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
#创建应用实例
edithomework = Blueprint('edithomework', __name__,  template_folder='templates')

@edithomework.route('/id/<int:id>', methods=['POST', 'GET'])
def homework_edit(id):
    homework = Homework.query.filter_by(id = id).first()
    if request.method == 'GET':
        print(homework)
        return render_template("Edithomework.html",\
        homework = homework,\
        role = session.get('role', 'unknow'),\
        username = session.get('username', ''),\
        id = id)
    if request.method == 'POST':
        print(request.form)
        #不为空
        if request.form.get('body', '') != '':
            #修改数据
            homework.body = request.form['body']
            #提交到数据库
            db.session.commit()
            #返回运行成功
            return 'Done'
        #修改失败
        return '233'

@edithomework.route('/answer/<int:id>', methods=['POST'])
def homework_answer(id):
    #旧的提交记录
    oldanswer = Answer.query.filter_by(homework_id = id).all()
    #没提交过
    if oldanswer == []:
        answer = Answer(request.form['body'], id)
        db.session.add(answer)
        db.session.commit()
        return 'Done'
    else:
        oldanswer[0].body = request.form['body']
        db.session.commit()
        return 'Done'
    return '233'

@edithomework.route('/score/<int:id>', methods=['POST'])
def homework_score(id):
    #找旧的分指表
    oldscore = Score.query.filter_by(homework_id = id).all()
    #没提交过
    if oldscore == []:
        score = Score(request.form['body'], id)
        db.session.add(score)
        db.session.commit()
        return 'Done'
    else:
        oldscore[0].body = request.form['body']
        db.session.commit()
        return 'Done'
    return '233'

#查看成绩
@edithomework.route('/score/watch/<int:id>', methods=['GET'])
def homework_score_watch(id):
    #有空做个排序
    scores = Score_Student.query.filter_by(homework_id = id).all()
    #(学生，成绩)的list
    score_list = []
    for i in scores:
        scoretext = i.body
        student = Student.query.filter_by(id = i.student_id).first()
        print(student)
        scoretext_list = scoretext.split("~")
        #这里len应该是固定的吧
        score_list.append((student, (scoretext_list[len(scoretext_list) - 1])))
    print(score_list)

    return render_template("Homework_Score_Watch.html",\
    score_list = score_list,\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id)
