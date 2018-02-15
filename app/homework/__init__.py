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
    if request.method == 'GET':
        homework = Homework.query.filter_by(id = id).first()
        print(homework)
        return render_template("Homework.html",\
        homework = homework,\
        role = session.get('role', 'unknow'),\
        username = session.get('username', ''),\
        id = id,\
        active = 2)
    if request.method == 'POST':
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
