from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
#创建应用实例
editcourses = Blueprint('editcourses', __name__,  template_folder='templates')

leftbarlist = (("indexpreview", "主页预览"),\
               ("coursewarelist", "课件列表"),\
               ("homework", "课后练习"),\
               ("experimentlist", "实验列表"),\
               ("studentlist", "学生列表"),\
               ("scoremanager", "成绩管理"))


@editcourses.route('/id/<int:id>', methods=['POST', 'GET'])
@editcourses.route('/id/<int:id>/indexpreview', methods=['POST', 'GET'])
def courseindex(id):
    currentcourses = Class.query.filter_by(id = id).first()
    if request.method == 'GET':
        return render_template("IndexPreview.html",\
        role = session.get('role', 'unknow'),\
        username = session.get('username', ''),\
        id = id,\
        currentcourses = currentcourses,\
        leftbar = leftbarlist,\
        active = 0)
    if request.method == 'POST':
        if request.form.get('introduction', '') != '':
            currentcourses.introduction = request.form['introduction']
            db.session.commit()
            return 'Done'
        return '233'


@editcourses.route('/id/<int:id>/coursewarelist', methods=['POST', 'GET'])
def coursewarelist(id):
    currentcourses = Class.query.filter_by(id = id).first()
    if request.method == 'GET':
        chapters = currentcourses.chapter.all()
        lessonlist = [[]]
        for chapter in chapters:
            chapterlist = []
            for lesson in chapter.lesson.all():
                chapterlist.append([lesson.name, lesson.id])
            lessonlist.append(chapterlist)
        return render_template("Coursewarelsit.html",\
        role = session.get('role', 'unknow'),\
        username = session.get('username', ''),\
        id = id,\
        chapter = chapters,\
        lessonlist = lessonlist,\
        leftbar = leftbarlist,\
        active = 1)
    if request.method == 'POST':
        if checkform_newchapter(request.form):
            index = currentcourses.chapter.count() + 1
            newChapter = Chapter(request.form['name'], request.form['introduction'], currentcourses.id, index)
            db.session.add(newChapter)
            db.session.commit()
            return 'Done'
        else:
            return '233'

def checkform_newchapter(form):
    if form.get('name', '') == '':
        return 0
    if form.get('introduction', '') == '':
        return 0
    return 1

#课后练习
@editcourses.route('/id/<int:id>/homework', methods=['POST', 'GET'])
def homework_editcourses(id):
    homeworks = Homework.query.filter_by(class_id = id).all()
    print(homeworks)
    return render_template("Homework_editcourses.html",\
    homeworks = homeworks,\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    leftbar = leftbarlist,\
    active = 2)


#实验列表
@editcourses.route('/id/<int:id>/experimentlist', methods=['POST', 'GET'])
def experiment(id):
    currentcourses = Class.query.filter_by(id = id).first()
    lesson = currentcourses.lesson.all()
    return render_template("Experimentlist.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    lesson = lesson,\
    leftbar = leftbarlist,\
    active = 3)

#学生列表
@editcourses.route('/id/<int:id>/studentlist', methods=['POST', 'GET'])
def studentlist(id):
    involed_class = Involed_class.query.filter_by(class_id = id).all()
    students = []
    for i in involed_class:
        students.append(i.student)
    return render_template("Studentlist.html",\
    students = students,\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    leftbar = leftbarlist,\
    active = 4)

#成绩管理
@editcourses.route('/id/<int:id>/scoremanager', methods=['POST', 'GET'])
def score(id):
    return render_template("Scoremanager.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    leftbar = leftbarlist,\
    active = 5)
