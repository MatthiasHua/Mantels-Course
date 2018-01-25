#课程管理库

#导入数据库模型
from app.model import *
#导入表单验证库
from app.modules.checkform import *

#创建新课程(通过表单)
#传入一个表单
#返回课程id
#如果为<0表示创建失败
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
            newsetting = Marksetting(0, 0, 0, 0, newclass.id)
            newclass.setting = newsetting.id
            #提交到数据库
            db.session.add(newsetting)
            db.session.commit()
            return 1
    else:
        return -1

#创建新课程(直接给参数)
#传入一个表单
#返回课程id
#如果为<0表示创建失败
def new_course(coursename, courseid, start, end, introduction, id):
    form = {'coursename': coursename,\
    'courseid': courseid,\
    'start': start,\
    'end': end,\
    'introduction': introduction,\
    'id': id}
    new_course_form(form)
