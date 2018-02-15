#课程管理库

#导入数据库模型
from app.model import *
#导入表单验证库
from app.modules.checkform import *

#---------------------------------------
#创建新课程(通过表单)
#输入:
#dict 表单
#     coursename   课程名称
#     courseid     课程代号(不是class_id)
#     start        课程开始时间
#     end          课程结束时间
#     introduction 课程介绍
#     id           setting_id
#输出:
#int: class_id 课程id 如果为<0表示创建失败
#---------------------------------------
def new_course_form(form):
    if checkform_new_course(form) == 1:
            #创建新课程(Class)
            newclass = Class(form['coursename'],\
            form['courseid'],\
            form['start'],\
            form['end'],\
            form['introduction'],\
            form['id'],\
            -1)
            #提交到数据库(为了获取id先提交一次)
            db.session.add(newclass)
            db.session.commit()
            #创建新的课程设定
            newsetting = Marksetting(1, 1, 1, 100, newclass.id)
            newclass.setting = newsetting.id
            #提交到数据库
            db.session.add(newsetting)
            db.session.commit()
            return 1
    else:
        return -1

#---------------------------------------
#创建新课程(直接给参数)
#输入:
#string: coursename   课程名称
#int:    courseid     课程代号(不是class_id)
#string: start        课程开始时间
#string: end          课程结束时间
#string: introduction 课程介绍
#int:    id           setting_id
#输出:
#int: class_id 课程id 如果为<0表示创建失败
#---------------------------------------
def new_course(coursename, courseid, start, end, introduction, id):
    form = {'coursename': coursename,\
    'courseid': courseid,\
    'start': start,\
    'end': end,\
    'introduction': introduction,\
    'id': id}
    return new_course_form(form)

#---------------------------------------
#学生数量
#输入:
#int: class_id 课程id
#输出:
#int: number 学生数量
#---------------------------------------
def get_number_of_student(class_id):
    return len(Involed_class.query.filter_by(class_id = class_id).all())
