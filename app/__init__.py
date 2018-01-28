import configparser
#日志
from app.logging import logging
#网络框架
from flask import Flask, session, render_template
#orm
from flask_sqlalchemy import SQLAlchemy

#设置文件
config = configparser.ConfigParser()
#读入设置
config.read("config.ini")

#建立网站实例
app = Flask(__name__)
#载入flask设置
app.config.from_object('config')

#初始化数据库
db = SQLAlchemy(app)
#导入数据库模型
from app.model import *

#登陆检查
from app import login_check

#主页
from app import index

#flask蓝图模块导入
from app.modules.blueprint import import_flask_blueprint
#载入Base中的框架
list(map(import_flask_blueprint, list(i for i in config.items("Base") if i[1] == "True")))
