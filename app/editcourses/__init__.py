from flask import Blueprint, render_template, redirect, url_for, request, session, make_response, Response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
#成绩管理库
from app.modules.mark import *
#时间管理库
from app.modules.time import *
import time
from datetime import datetime
#创建应用实例
import tablib
from urllib.parse import quote
editcourses = Blueprint('editcourses', __name__,  template_folder='templates')

leftbarlist = (("indexpreview", "主页预览"),\
               ("coursewarelist", "课件列表"),\
               ("homework", "课后练习"),\
               ("experimentlist", "实验列表"),\
               ("studentlist", "学生列表"),\
               ("scoremanager", "成绩管理"),\
               ("insertscore", "添加成绩（test)"),\
               ("scorewatch", "查看成绩"))

#主页预览
@editcourses.route('/id/<int:id>', methods=['POST', 'GET'])
@editcourses.route('/id/<int:id>/indexpreview', methods=['POST', 'GET'])
def courseindex(id):
    currentcourses = Class.query.filter_by(id = id).first()
    if request.method == 'GET':
        announcements = Announcement.query.filter_by(class_id = id).order_by(Announcement.time.desc()).all()
        announcementlist = []
        for i in announcements:
            print(i.body)
            announcementlist.append((i.body, datetime.fromtimestamp(i.time).strftime("%Y-%m-%d %H:%M")))
        return render_template("IndexPreview.html",\
        role = session.get('role', 'unknow'),\
        username = session.get('username', ''),\
        id = id,\
        currentcourses = currentcourses,\
        announcements = announcementlist,\
        leftbar = leftbarlist,\
        active = 0)
    if request.method == 'POST':
        if request.form.get('introduction', '') != '':
            currentcourses.introduction = request.form['introduction']
            db.session.commit()
            return 'Done'
        return '233'

#新公告 post
@editcourses.route('/id/<int:id>/new_announcement', methods=['POST'])
def new_announcement(id):
    if request.form.get('announcement', '') != '':
        new_announcement = Announcement(id, request.form['announcement'], int(time.time()))
        db.session.add(new_announcement)
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
    state_list = []
    print(homeworks)
    for i in homeworks:
        state_list.append(check_homework_state(i.id))
    return render_template("Homework_editcourses.html",\
    homeworks = homeworks,\
    state_list = state_list,\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    leftbar = leftbarlist,\
    active = 2)

#创建新的课后练习
@editcourses.route('/id/<int:id>/newhomework', methods=['POST'])
def newhomework_editcourses(id):
    #index貌似没什么用了。。
    newHomework = Homework(id, -1, request.form.get('name', ''), request.form.get('body', ''), request.form.get('start', ''), request.form.get('end', ''))
    db.session.add(newHomework)
    db.session.commit()
    return "Done"

#实验列表
@editcourses.route('/id/<int:id>/experimentlist', methods=['POST', 'GET'])
def experiment(id):
    return render_template("Experimentlist.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
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
#修改设定的界面
@editcourses.route('/id/<int:id>/scoremanager', methods=['GET'])
def score(id):
    return render_template("Scoremanager.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    leftbar = leftbarlist,\
    active = 5)

#修改设定
@editcourses.route('/id/<int:id>/changesetting', methods=['POST'])
def changesetting(id):
    oldsetting = Marksetting.query.filter_by(class_id = id).first()
    oldsetting.attendance = request.form.get('attendance', '')
    oldsetting.homework = request.form.get('homework', '')
    oldsetting.examination = request.form.get('examination', '')
    oldsetting.total = request.form.get('total', '')
    db.session.commit()
    return "Done"

#添加成绩的界面
@editcourses.route('/id/<int:id>/insertscore', methods=['GET'])
def insertscore(id):
    return render_template("Insertscore.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    leftbar = leftbarlist,\
    active = 6)

#添加成绩(post)
@editcourses.route('/id/<int:id>/insertscore_post', methods=['POST'])
def insertscore_post(id):
    newmark = Mark(request.form.get("mark", ""),\
    request.form.get("type", ""),\
    request.form.get("student_id", ""),\
    id)
    db.session.add(newmark)
    db.session.commit()
    return "Done"

#查看成绩
@editcourses.route('/id/<int:id>/scorewatch', methods=['POST', 'GET'])
def scorewatch(id):
    mark_list = update_mark_class_total(id, 1)
    return render_template("Scorewatch.html",\
    mark_list = mark_list,\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    leftbar = leftbarlist,\
    active = 7)

#下载成绩
@editcourses.route('/id/<int:id>/scoreexcel', methods=['POST', 'GET'])
def testexcel(id):
    headers = ("学号", "姓名", "成绩")
    mark_list = update_mark_class_total(id, 1)
    data = tablib.Dataset(*mark_list, headers=headers)
    response = make_response(data.xls)
    response.headers["Content-Disposition"] = "attachment; filename*=utf-8''{}".format(quote(Class.query.filter_by(id = id).first().coursename + "成绩.xls"))
    return response
