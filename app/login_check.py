from flask import request, session, redirect, url_for
from app import app

#登陆检查
@app.before_request
def check_need_login():
    print(request.endpoint)
    if request.endpoint.split('.')[0] in ('wechat', 'wechatcoursewares', 'api'):
        return
    #教师限制访问
    if session.get('role', '') == 'Teacher' and session.get('admin', '') !=  9:
        allowlist = ('teacher', 'teachercenter', 'editcourses', 'editcoursewares', 'edithomework',\
        'courses', 'coursewares', 'markdowneditor', 'user_base', 'about', 'help', 'index')
        if request.endpoint.split('.')[0] not in allowlist:
            return redirect(url_for('index'))
    #学生限制访问
    if session.get('role', '') == 'Student':
        allowlist = ('student', 'studentcenter',\
        'courses', 'coursewares', 'markdowneditor', 'user_base', 'about', 'help', 'index')
        if request.endpoint.split('.')[0] not in allowlist:
            return redirect(url_for('student.studentindex'))
