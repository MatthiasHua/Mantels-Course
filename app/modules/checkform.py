#表单验证库

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
#int: result       为1时表单合法，否则返回错误代码
#---------------------------------------
def checkform_new_lesson(name, body, chapter_id, index):
    if name == '':
        return -1
    if body == '':
        return -1
    if chapter_id == '':
        return -1
    return 1
