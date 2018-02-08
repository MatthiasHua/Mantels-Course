from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
from app.modules.key import *
from app.modules.mail import *
import time
#创建应用实例
teachercenter = Blueprint('teachercenter', __name__,  template_folder='templates')

leftbarlist = (("teacherbasicinfo", "基本信息"),\
               ("changepassword", "修改密码"),\
               ("token", "安全令牌"))

#基本信息
#显示用户名和邮箱
@teachercenter.route('/', methods=['POST', 'GET'])
@teachercenter.route('/index', methods=['POST', 'GET'])
@teachercenter.route('/teacherbasicinfo', methods=['POST', 'GET'])
def teacherbasicinfo():
    user = Teacher.query.filter_by(username = session['username']).first()
    email_check = user.email_check
    #用户名：user.username或者session.get('username', '')
    #邮箱:user.email
    return render_template("TeacherBasicInfo.html",\
	role = session.get('role', ''),\
	username = session.get('username', ''),\
    email = user.email,\
    email_check = email_check,\
    leftbar = leftbarlist,\
    active = 0)

@teachercenter.route('/check_email', methods=['POST'])
def check_email_teacher():
    user = Teacher.query.filter_by(username = session['username']).first()
    email = user.email
    email_check = user.email_check
    if email_check == 1:
        return 'already checked'
    old = Email_check_key_teacher.query.filter_by(teacher_id = session['id']).all()
    key = create_key(16)
    if old == []:
        new = Email_check_key_teacher(session['id'], key, int(time.time()) + 1800)
        db.session.add(new)
    else:
        new = old[0]
        new.time = int(time.time()) + 1800;
        new.key = key
    db.session.commit()
    send_email(email, "Mantels邮箱验证", "请在半小时内点击以下链接对邮箱账号进行验证: <br>mantels.top/api/check_email/teacher/" + key + "<br>如果不是您本人操作，请不要点击此链接！")
    #用户名：user.username或者session.get('username', '')
    #邮箱:user.email
    return 'Done'

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
        user = Teacher.query.filter_by(username = session['username']).first()
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

@teachercenter.route('/token', methods=['GET'])
def token():
    if Token.query.filter_by(teacher_id = session["id"]).all() == []:
        open = False
    else:
        open = True
    print(open)
    return render_template("Token.html",\
    open = open,\
	role = session.get('role', ''),\
	username = session.get('username', ''),\
    leftbar = leftbarlist,\
    active = 2)

@teachercenter.route('/gettoken', methods=['POST'])
def gettoken():
    newtoken = create_key(16)
    if Token.query.filter_by(teacher_id = session["id"]).all() == []:
        token = Token(session["id"], newtoken)
        db.session.add(token)
    else:
        token = Token.query.filter_by(teacher_id = session["id"]).first()
        print(token)
        token.content = newtoken
    db.session.commit()
    return newtoken


#需要对表单进行验证
#现在只简单确认表单不为空
def checkform_changepassword(form):
    user = Teacher.query.filter_by(username = session['username']).first()
    if form['oldpassword'] != user.password:
        return False
    if form['newpassowrd'] == '':
        return False
    return True
