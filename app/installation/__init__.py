from flask import Blueprint, render_template, redirect, url_for, request
#根目录下config.ini
from app import config

#创建应用实例
installation = Blueprint('installation', __name__,  template_folder='templates')

#主页
@installation.route('/')
@installation.route('/index')
def index():
    return render_template("Welcome.html", url1 = url_for("installation.license"))

#许可证协议
from app.installation import license

#安装包管理
from app.installation import packagemanager

@installation.route('/packageindex')
def packageindex():
    return "packageindex!"

