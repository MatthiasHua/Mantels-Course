#表单验证库
import re

rule = {
'number': '^\d{6,12}$',
'username': '^[\u4e00-\u9fa5a-zA-Z\s]{2,30}$',
'courses': '^[\u4e00-\u9fa5a-zA-Z\s]{2,30}$',
'email': '^[0-9a-zA-Z_\.]{0,20}@[0-9a-zA-Z_\.]{1,15}\.[a-zA-Z]{1,5}$',
'password': '[0-9a-zA-Z]{6,20}',
}

#---------------------------------------
#验证新课程的表单
#输入:
#dict 表单
#     coursename   课程名称
#     courseid     课程代号(不是class_id)
#     start        课程开始时间
#     end          课程结束时间
#     introduction 课程介绍
#     id           setting_id
#输出:
#int: result       为1时表单合法，否则返回错误代码
#---------------------------------------
def checkform_new_course(form):
    if form.get('coursename', '') == '':
        return -1
    if form.get('courseid', '') == '':
        return -1
    if form.get('start', '') == '':
        return -1
    if form.get('end', '') == '':
        return -1
    if form.get('introduction', '') == '':
        return -1
    if form.get('id', '') == '':
        return -1
    return 1

#---------------------------------------
#验证新课件的表单
#输入:
#dict 表单
#string: name 课件名称
#string: body 课件内容
#int: chapter_id 章节id
#输出:
#int: result       为1时表单合法
#---------------------------------------
def checkform_new_lesson(name, body, chapter_id, index):
    if name == '':
        return -1
    if body == '':
        return -1
    if chapter_id == '':
        return -1
    return 1

#---------------------------------------
#验证注册新教师的表单
#输入:
#dict 表单
#输出:
#int: result       为1时表单合法
#-1 账号不合法
#-2 用户名不合法
#-3 密码不合法
#-4 邮箱不合法
#---------------------------------------
def new_teacher(form):
    list = ['number', 'username', 'password', 'email']
    return checkform(list, form)

#---------------------------------------
#验证注册新学生的表单
#输入:
#dict 表单
#输出:
#int: result       为1时表单合法
#-1 账号不合法
#-2 用户名不合法
#-3 密码不合法
#-4 邮箱不合法
#---------------------------------------
def new_student(form):
    list = ['number', 'username', 'password', 'email']
    return checkform(list, form)

#---------------------------------------
#通用表单验证
#输入:
#list 需要验证的项
#dict 表单
#输出:
#int: result
#---------------------------------------
def checkform(list, form):
    for i in range(len(list)):
        if re.match(rule[list[i]], form[list[i]]) == None:
            return -i-1
    return 1
