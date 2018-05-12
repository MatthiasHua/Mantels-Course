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
        #state_list.append(check_homework_state(i.id))
        state_list.append(1)
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
    body = request.form.get('body', '')
    newHomework = Homework(request.form.get('name', ''), 1, 6, id, request.form.get('start', ''), request.form.get('end', ''), 50)
    db.session.add(newHomework)
    db.session.commit()
    questions = body.split("~~")
    index = 0
    questions.remove("")
    for question in questions:
        index = index + 1
        type = question.split("-")[0]
        score = question.split("-")[1]
        question = question[question.index("-") + 1 :]
        question = question[question.index("-") + 1 :]
        print(question)
        q = Question(index, newHomework.id, type, score, question)
        db.session.add(q)
    db.session.commit()
    return "Done"

#实验列表
@editcourses.route('/id/<int:id>/experimentlist', methods=['POST', 'GET'])
def experiment(id):
    experiments = Experiment.query.filter_by(class_id = id).all()
    print(experiments)
    return render_template("Experimentlist.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    experiments = experiments,\
    id = id,\
    leftbar = leftbarlist,\
    active = 3)

@editcourses.route('/id/<int:id>/set_current_experiment', methods=['POST'])
def set_current_experiment(id):
    experiment_id = request.form.get("experiment_id")
    find = Experiment.query.filter_by(id = experiment_id).first()
    if find == None :
        return "404"
    else :
        if find.current == 0 :
            old_current = Experiment.query.filter_by(class_id = id, current = 1).first()
            if old_current != None :
                old_current.current = 0
        find.current = (find.current + 1) % 2
        db.session.commit()
        now = Current_Experiment.query.filter_by(class_id = id).first()
        if now == None :
            new_current_experiment = Current_Experiment(id, experiment_id)
            db.session.add(new_current_experiment)
            db.session.commit()
        else :
            if find.current == 0 :
                now.experiment_id = 0
            else :
                now.experiment_id = experiment_id
            db.session.commit()
        return "success"

#添加实验
@editcourses.route('/id/<int:id>/newexperiment', methods=['POST'])
def newexperiment(id):
    if request.form.get('name', '') != '':
        newExperiment = Experiment(id, session['id'], request.form['name'])
        db.session.add(newExperiment)
        db.session.commit()
        return 'Done'
    return '233'

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
