from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
#创建应用实例
editcoursewares = Blueprint('editcoursewares', __name__,  template_folder='templates')


@editcoursewares.route('/id/<int:id>/chapter/<int:chapter>', methods=['POST', 'GET'])
def editbychapter(id, chapter):
    currentcourses = Class.query.filter_by(id = id).first()
    chapters = currentcourses.chapter.all()
    currentchapter = currentcourses.chapter.filter_by(index = chapter).first()
    if request.method == 'GET':
        lessons = currentchapter.lesson.all()
        return render_template("EditbyChapter.html",\
        chapters = chapters,\
        lessons = lessons,\
        role = session.get('role', 'unknow'),\
        username = session.get('username', ''),\
        id = id,\
        introduction = currentchapter.introduction,\
        chapter = chapter - 1)
    if request.method == 'POST':
        print(request.form)
        if request.form.get('introduction', '') != '':
            currentchapter.introduction = request.form['introduction']
            db.session.commit()
            return 'Done'
        return '233'


@editcoursewares.route('/id/<int:id>/chapter/<int:chapter>/lesson/<int:lesson>', methods=['POST', 'GET'])
def editbylesson(id, chapter, lesson):
    currentcourses = Class.query.filter_by(id = id).first()
    chapters = currentcourses.chapter.all()
    currentchapter = currentcourses.chapter.filter_by(index = chapter).first()
    if request.method == 'GET':
        lessons = currentchapter.lesson.all()
        body = currentchapter.lesson.filter_by(index = lesson).first().body
        return render_template("EditbyLesson.html",\
        chapters = chapters,\
        lessons = lessons,\
        role = session.get('role', 'unknow'),\
        username = session.get('username', ''),\
        id = id,\
        body = body,\
        currentcourses = currentcourses,\
        chapter = chapter - 1,\
        lesson = lesson)
    if request.method == 'POST':
        print(request.form)
        if request.form.get('body', '') != '':
            currentlesson = currentchapter.lesson.filter_by(index = lesson).first()
            currentlesson.body = request.form['body']
            db.session.commit()
            return 'Done'
        return '233'
