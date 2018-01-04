from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
#创建应用实例
coursewares = Blueprint('coursewares', __name__,  template_folder='templates')


@coursewares.route('/id/<int:id>/chapter/<int:chapter>', methods=['POST', 'GET'])
def editbychapter(id, chapter):
    currentcourses = Class.query.filter_by(id = id).first()
    chapters = currentcourses.chapter.all()
    currentchapter = currentcourses.chapter.filter_by(index = chapter).first()
    lessons = currentchapter.lesson.all()
    return render_template("Courseware_Chapter.html",\
    chapters = chapters,\
    lessons = lessons,\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    introduction = currentchapter.introduction,\
    chapter = chapter - 1)


@coursewares.route('/id/<int:id>/chapter/<int:chapter>/lesson/<int:lesson>', methods=['POST', 'GET'])
def editbylesson(id, chapter, lesson):
    currentcourses = Class.query.filter_by(id = id).first()
    chapters = currentcourses.chapter.all()
    currentchapter = currentcourses.chapter.filter_by(index = chapter).first()
    lessons = currentchapter.lesson.all()
    body = currentchapter.lesson.filter_by(index = lesson).first().body
    return render_template("Courseware_Lesson.html",\
    chapters = chapters,\
    lessons = lessons,\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    body = body,\
    currentcourses = currentcourses,\
    chapter = chapter - 1,\
    lesson = lesson)
