from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
from app.modules.courseware import *
#创建应用实例
editcoursewares = Blueprint('editcoursewares', __name__,  template_folder='templates')


@editcoursewares.route('/id/<int:id>/chapter/<int:chapter>', methods=['POST', 'GET'])
def editbychapter(id, chapter):
    #当前页所指的课程
    currentcourses = Class.query.filter_by(id = id).first()
    #当前课程的所有章节
    chapters = currentcourses.chapter.all()
    #当前页所指的章节
    currentchapter = currentcourses.chapter.filter_by(index = chapter).first()
    #返回页面
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
    #接收到表单
    #这一页三个按钮
    #修改章节导引

    #修改章节名称

    #添加新课件
    if request.method == 'POST':
        print(request.form)
        #不为空
        if request.form.get('introduction', '') != '':
            #修改数据
            currentchapter.introduction = request.form['introduction']
            #提交到数据库
            db.session.commit()
            #返回运行成功
            return 'Done'
        #修改失败
        return '233'

#修改章节名称
@editcoursewares.route('/id/<int:id>/changechaptername/<int:chapter>', methods=['POST'])
def changechaptername(id, chapter):
    #当前页所指的课程
    currentcourses = Class.query.filter_by(id = id).first()
    #当前课程的所有章节
    chapters = currentcourses.chapter.all()
    #当前页所指的章节
    currentchapter = currentcourses.chapter.filter_by(index = chapter).first()
    print(request.form)
    #不为空
    if request.form.get('name', '') != '':
        #修改数据
        currentchapter.name = request.form['name']
        #提交到数据库
        db.session.commit()
        #返回运行成功
        return 'Done'
    #修改失败
    return '233'

#添加新课件
@editcoursewares.route('/id/<int:id>/newlesson/<int:chapter>', methods=['POST'])
def newlesson(id, chapter):
    index = get_number_of_lesson(id, chapter)
    chapter_id = get_current_chapter(id, chapter).id
    if new_lesson(request.form.get('name', ''), request.form.get('body', ''), chapter_id, index) == 1:
        return 'Done'
    #修改失败
    return '233'

@editcoursewares.route('/id/<int:id>/chapter/<int:chapter>/lesson/<int:lesson>', methods=['POST', 'GET'])
def editbylesson(id, chapter, lesson):
    #当前页所指的课程
    currentcourses = Class.query.filter_by(id = id).first()
    #当前课程的所有章节
    chapters = currentcourses.chapter.all()
    #当前页所指的章节
    currentchapter = currentcourses.chapter.filter_by(index = chapter).first()
    if request.method == 'GET':
        #当前章节的所有Lesson
        lessons = currentchapter.lesson.all()
        #当前课的内容
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
    #接收到表单
    #这一页两个个按钮
    #修改课件内容
    #修改课件标题
    if request.method == 'POST':
        print(request.form)
        #不为空
        if request.form.get('body', '') != '':
            currentlesson = currentchapter.lesson.filter_by(index = lesson).first()
            #修改数据
            currentlesson.body = request.form['body']
            db.session.commit()
            #返回运行成功
            return 'Done'
        #修改失败
        return '233'

@editcoursewares.route('/id/<int:id>/chapter/<int:chapter>/lesson/changename/<int:lesson>', methods=['POST', 'GET'])
def changelessonname(id, chapter, lesson):
    #当前页所指的课程
    currentcourses = Class.query.filter_by(id = id).first()
    #当前课程的所有章节
    chapters = currentcourses.chapter.all()
    #当前页所指的章节
    currentchapter = currentcourses.chapter.filter_by(index = chapter).first()

    if request.method == 'POST':
        print(request.form)
        #不为空
        if request.form.get('name', '') != '':
            currentlesson = currentchapter.lesson.filter_by(index = lesson).first()
            #修改数据
            currentlesson.name = request.form['name']
            db.session.commit()
            #返回运行成功
            return 'Done'
        #修改失败
        return '233'
