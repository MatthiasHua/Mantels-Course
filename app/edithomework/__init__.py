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
        id = id,\
        active = 2)
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
