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
    questions = Question.query.filter_by(homework_id = id).order_by(Question.index).all()
    if request.method == 'GET':
        return render_template("Edithomework.html",\
        homework = homework,\
        questions = questions,\
        role = session.get('role', 'unknow'),\
        username = session.get('username', ''),\
        id = id)
    if request.method == 'POST':
        form = request.form
        question_id = questions[int(form.get('question')) - 1].id
        if form.get('question', '') == '':
            return 'question id miss'
        if form.get('content', '') == '' or form.get('content') == None:
            return 'content id miss'
        oldsolution = Solution.query.filter_by(question_id = question_id).first()
        if oldsolution == None:
            solution = Solution(question_id, form.get('content'))
            db.session.add(solution)
        else:
            oldsolution.content = form.get('content')
        db.session.commit()
        return 'Done'

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
    scores = Score.query.filter_by(type = "homework", index = id).all()
    sumscore = Homework.query.filter_by(id = id).first().score
    #(学生，成绩)的list
    score_list = []
    for i in scores:
        student = Student.query.filter_by(id = i.student_id).first()
        score_list.append((student, i.value))
    print(score_list)

    return render_template("Homework_Score_Watch.html",\
    score_list = score_list,\
    sumscore = sumscore,\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id)
