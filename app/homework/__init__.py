from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
#创建应用实例
homework = Blueprint('homework', __name__,  template_folder='templates')

@homework.route('/id/<int:id>', methods=['POST', 'GET'])
def homework_edit(id):
    homework = Homework.query.filter_by(id = id).first()
    questions = Question.query.filter_by(homework_id = id).order_by(Question.index).all()
    if request.method == 'GET':
        return render_template("Homework.html",\
        homework = homework,\
        questions = questions,\
        role = session.get('role', 'unknow'),\
        username = session.get('username', ''),\
        id = id,\
        active = 2)
    if request.method == 'POST':
        form = request.form
        question_id = questions[int(form.get('question')) - 1].id
        if form.get('question', '') == '':
            return 'question id miss'
        if form.get('content', '') == '' or form.get('content') == None:
            return 'content id miss'
        oldanswer = Answer.query.filter_by(question_id = question_id, student_id = session.get('id')).first()
        if oldanswer == None:
            answer = Answer(question_id, session.get('id'), form.get('content'))
            db.session.add(answer)
        else:
            oldanswer.content = form.get('content')
        db.session.commit()
        return 'Done'
        '''
        if request.form.get('body', '') != '':
            #旧的提交记录
            oldanswer = Answer_Student.query.filter_by(homework_id = id, student_id = session.get('id', '')).all()
            #没提交过
            if oldanswer == []:
                answer = Answer_Student(request.form['body'], session.get('id', ''), id)
                db.session.add(answer)
                db.session.commit()
                return 'Done'
            else:
                oldanswer[0].body = request.form['body']
                db.session.commit()
                return 'Done'
        print(request.form)
        return "233"
        '''
