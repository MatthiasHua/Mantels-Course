from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
from werkzeug.utils import secure_filename
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db, basepath
from app.modules.face import *
from app.modules.key import *
from app.modules.mail import *
import os
import time

#创建应用实例
studentcenter = Blueprint('studentcenter', __name__,  template_folder='templates')

leftbarlist = (("studentbasicinfo", "基本信息"),\
               ("changepassword", "修改密码"),\
               ("face", "开启人脸识别"),\
               ("signin_face", "测试人脸登录"))

#基本信息
#显示用户名和邮箱
@studentcenter.route('/', methods=['POST', 'GET'])
@studentcenter.route('/index', methods=['POST', 'GET'])
@studentcenter.route('/studentbasicinfo', methods=['POST', 'GET'])
def studentbasicinfo():
    user = Student.query.filter_by(username = session['username']).first()
    email_check = user.email_check
    #用户名：user.username或者session.get('username', '')
    #邮箱:user.email
    return render_template("StudentBasicInfo.html",\
	role = session.get('role', ''),\
	username = session.get('username', ''),\
    email = user.email,\
    email_check = email_check,\
    leftbar = leftbarlist,\
    active = 0)

@studentcenter.route('/check_email', methods=['POST'])
def check_email_student():
    user = Student.query.filter_by(username = session['username']).first()
    email = user.email
    email_check = user.email_check
    if email_check == 1:
        return 'already checked'
    old = Email_check_key_student.query.filter_by(student_id = session['id']).all()
    key = create_key(16)
    if old == []:
        new = Email_check_key_student(session['id'], key, int(time.time()) + 1800)
        db.session.add(new)
    else:
        new = old[0]
        new.time = int(time.time()) + 1800;
        new.key = key
    db.session.commit()
    send_email(email, "Mantels邮箱验证", "请在半小时内点击以下链接对邮箱账号进行验证: <br>mantels.top/api/check_email/student/" + key + "<br>如果不是您本人操作，请不要点击此链接！")
    #用户名：user.username或者session.get('username', '')
    #邮箱:user.email
    return 'Done'


#修改密码
#需要输入旧密码和新密码
#表单中旧密码名字为oldpassword
#     新密码名字为newpassword
@studentcenter.route('/changepassword', methods=['POST', 'GET'])
def changepassword():
    #这里返回的是界面
    if request.method == 'GET':
        return render_template("ChangePassword_Student.html",\
    	role = session.get('role', ''),\
    	username = session.get('username', ''),\
        leftbar = leftbarlist,\
        active = 1)
    #验证并修改密码
    if request.method == 'POST':
        user = Student.query.filter_by(username = session['username']).first()
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


#开启人脸识别
@studentcenter.route('/face', methods=['POST', 'GET'])
def student_face_open():
    if request.method == 'GET':
        user = Student.query.filter_by(username = session['username']).first()
        #用户名：user.username或者session.get('username', '')
        #邮箱:user.email
        return render_template("Uploadfacepic.html",\
    	role = session.get('role', ''),\
    	username = session.get('username', ''),\
        email = user.email,\
        leftbar = leftbarlist,\
        active = 2)
    if request.method == 'POST':
        f = request.files['file']
        fname = f.filename
        ext = fname.rsplit('.', 1)[1]
        if not ext in ('jpg', 'png', 'bmp'):
            return "格式错误"
        upload_path = os.path.join(basepath, 'pic\\face', str(session['id']) + '.' + ext)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        return "上传成功，当前处于测试版可能无法在网站上看到成功状态"

#测试登录
@studentcenter.route('/signin_face', methods=['POST', 'GET'])
def student_signin_face():
    if request.method == 'GET':
        user = Student.query.filter_by(username = session['username']).first()
        #用户名：user.username或者session.get('username', '')
        #邮箱:user.email
        return render_template("Signin_Face_Studentcenter.html",\
    	role = session.get('role', ''),\
    	username = session.get('username', ''),\
        email = user.email,\
        leftbar = leftbarlist,\
        active = 3)
    if request.method == 'POST':
        f = request.files['file']
        fname = f.filename
        ext = fname.rsplit('.', 1)[1]
        if not ext in ('jpg', 'png', 'bmp'):
            return "格式错误"
        upload_path = os.path.join(basepath, 'pic\\testlogin', str(session['id']) + '.' + ext)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        return "上传成功，当前处于测试版可能无法在网站上看到成功状态"

#测试登录
@studentcenter.route('/signin_face_test', methods=['POST'])
def student_signin_face_test():
    r = test_compare('\\pic\\face\\' + str(session['id']) + '.jpg', '\\pic\\testlogin\\' + str(session['id']) + '.jpg')
    return str(r)

#需要对表单进行验证
#现在只简单确认表单不为空
def checkform_changepassword(form):
    user = Student.query.filter_by(username = session['username']).first()
    if form['oldpassword'] != user.password:
        return False
    if form['newpassowrd'] == '':
        return False
    return True
