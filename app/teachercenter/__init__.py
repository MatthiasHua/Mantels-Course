from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
#创建应用实例
teachercenter = Blueprint('teachercenter', __name__,  template_folder='templates')

leftbarlist = (("teacherbasicinfo", "基本信息"),\
               ("changepassword", "修改密码"))

#基本信息
#显示用户名和邮箱
@teachercenter.route('/', methods=['POST', 'GET'])
@teachercenter.route('/index', methods=['POST', 'GET'])
@teachercenter.route('/teacherbasicinfo', methods=['POST', 'GET'])
def teacherbasicinfo():
    user = User.query.filter_by(username = session['username']).first()
    #用户名：user.username或者session.get('username', '')
    #邮箱:user.email
    return render_template("TeacherBasicInfo.html",\
	role = session.get('role', ''),\
	username = session.get('username', ''),\
    email = user.email,\
    leftbar = leftbarlist,\
    active = 0)

#修改密码
#需要输入旧密码和新密码
#表单中旧密码名字为oldpassword
#     新密码名字为newpassword
@teachercenter.route('/changepassword', methods=['POST', 'GET'])
def changepassword():
    #这里返回的是界面
    if request.method == 'GET':
        return render_template("ChangePassword.html",\
    	role = session.get('role', ''),\
    	username = session.get('username', ''),\
        leftbar = leftbarlist,\
        active = 1)
    #验证并修改密码
    if request.method == 'POST':
        user = User.query.filter_by(username = session['username']).first()
        print(request.form)
        #验证旧密码是否正确和新密码是否合法
        if checkform_changepassword(request.form):
            #修改密码
            user.password = request.form['newpassowrd']
            #提交到数据库
            db.session.commit()
            #返回创建课程成功
            return "Done"
        else:
            #创建课程失败
            return "233"

#需要对表单进行验证
#现在只简单确认表单不为空
def checkform_changepassword(form):
    user = User.query.filter_by(username = session['username']).first()
    if form['oldpassword'] != user.password:
        return False
    if form['newpassowrd'] == '':
        return False
    return True
