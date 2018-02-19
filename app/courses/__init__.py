from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
from datetime import datetime
#创建应用实例
courses = Blueprint('courses', __name__,  template_folder='templates')

leftbarlist = (("courseindex", "课程主页"),\
               ("courseware", "课件"),\
               ("homework", "习题"),\
               ("experiment", "实验"),\
               ("score", "成绩"))

#主页
@courses.route('/', methods=['POST', 'GET'])
@courses.route('/index', methods=['POST', 'GET'])
def coursesindex():
    return render_template("StudentIndex.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    leftbar = leftbarlist,\
    active = 0)

@courses.route('/id/<int:id>', methods=['POST', 'GET'])
@courses.route('/id/<int:id>/courseindex', methods=['POST', 'GET'])
def courseindex(id):
    currentcourses = Class.query.filter_by(id = id).first()
    announcements = Announcement.query.filter_by(class_id = id).order_by(Announcement.time.desc()).all()
    announcementlist = []
    for i in announcements:
        print(i.body)
        announcementlist.append((i.body, datetime.fromtimestamp(i.time).strftime("%Y-%m-%d %H:%M")))
    print(currentcourses)
    return render_template("CoursesIndex.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    currentcourses = currentcourses,\
    announcements = announcementlist,\
    leftbar = leftbarlist,\
    active = 0)

@courses.route('/id/<int:id>/courseware', methods=['POST', 'GET'])
def courseware(id):
    currentcourses = Class.query.filter_by(id = id).first()
    chapters = currentcourses.chapter.all()
    lessonlist = [[]]
    for chapter in chapters:
        chapterlist = []
        for lesson in chapter.lesson.all():
            print(lesson.name, lesson.id)
            chapterlist.append([lesson.name, lesson.id])
        lessonlist.append(chapterlist)
    return render_template("Courseware.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    chapter = chapters,\
    lessonlist = lessonlist,\
    leftbar = leftbarlist,\
    active = 1)

#习题
@courses.route('/id/<int:id>/homework', methods=['POST', 'GET'])
def homework_courses(id):
    homeworks = Homework.query.filter_by(class_id = id).all()
    print(homeworks)
    return render_template("Homework_courses.html",\
    homeworks = homeworks,\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    leftbar = leftbarlist,\
    active = 2)

@courses.route('/id/<int:id>/experiment', methods=['POST', 'GET'])
def experiment(id):
    experiments = Experiment.query.filter_by(class_id = id).all()
    return render_template("Experiment.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    experiments = experiments,\
    id = id,\
    leftbar = leftbarlist,\
    active = 3)

@courses.route('/id/<int:id>/score', methods=['POST', 'GET'])
def score(id):
    return render_template("Score.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    leftbar = leftbarlist,\
    active = 4)
