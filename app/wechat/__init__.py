from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
from app import config
import hashlib

#xml解析
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


#创建应用实例
wechat = Blueprint('wechat', __name__,  template_folder='templates')

@wechat.route('/', methods=['POST', 'GET'])
@wechat.route('/index', methods=['POST', 'GET'])
def wechatindex():
    # 判断请求方式是GET请求
    if request.method == "GET":

        #从config.ini中读取token
        for i in config.items("Wechat"):
            if i[0] == 'token':
                token = i[1]
        print(token)

        my_signature = request.args.get('signature')     # 获取携带的signature参数
        my_timestamp = request.args.get('timestamp')     # 获取携带的timestamp参数
        my_nonce = request.args.get('nonce')        # 获取携带的nonce参数
        my_echostr = request.args.get('echostr')         # 获取携带的echostr参数

        # 进行字典排序
        data = [token,my_timestamp ,my_nonce ]
        data.sort()

        # 拼接成字符串
        temp = ''.join(data)

        # 进行sha1加密
        mysignature = hashlib.sha1(temp.encode("utf8")).hexdigest()

        # 加密后的字符串可与signature对比，标识该请求来源于微信
        if my_signature == mysignature:
            return my_echostr

    if request.method == "POST":
        print("post")
        print(request.args)
        print(request.form)
        print(request.get_data('content'))
        xmlcontent = request.get_data('content')
        root = ET.fromstring(xmlcontent)
        print(root.tag)
        print(root[0].tag)
        for i in root:
            if i.tag == 'Content':
                print(i.text)
        return "success"
