#课件相关

from app.modules.checkform import *
from app import db
from app.model import *

#---------------------------------------
#创建新课件(通过表单)
#输入:
#dict 表单
#string: name 课件名称
#string: body 课件内容
#int: chapter_id 章节id
#int index 序号
#输出:
#int: result       为1时创建成功，否则返回错误代码
#---------------------------------------
def new_lesson(name, body, chapter_id, index):
    if checkform_new_lesson(name, body, chapter_id, index) == 1:
            #创建新课件(Lesson)
            newlesson = Lesson(name, body, chapter_id, index)
            #提交到数据库
            db.session.add(newlesson)
            db.session.commit()
            return 1
    else:
        return -1

#---------------------------------------
#获取当前课程
#输入:
#int: class_id
#输出:
#Chapter: currentcourse 当前课程
#---------------------------------------
def get_current_chapter(cladd_id, chapter):
    return Class.query.filter_by(id = class_id).first()

#---------------------------------------
#获取当前章节
#输入:
#int id
#int: chapter
#输出:
#Chapter: currentchapter 当前章节
#---------------------------------------
def get_current_chapter(id, chapter):
    currentcourses = Class.query.filter_by(id = id).first()
    chapters = currentcourses.chapter.all()
    currentchapter = currentcourses.chapter.filter_by(index = chapter).first()
    return currentchapter

#---------------------------------------
#获取当前章节课件数
#输入:
#int: id
#int: chapter
#输出:
#Chapter: number 当前章节课件数
#---------------------------------------
def get_number_of_lesson(id, chapter):
    chapter = get_current_chapter(id, chapter)
    return Lesson.query.filter_by(chapter_id = chapter.id).count()
