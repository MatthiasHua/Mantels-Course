from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
from time import time
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
        #接受微信消息
        xmlcontent = request.get_data('content')
        print(xmlcontent)
        #解析XML
        root = ET.fromstring(xmlcontent)

        #接收文本消息
        #范例:
        #<xml>
        #  <ToUserName>
        #    < ![CDATA[toUser] ]>
        #  </ToUserName>
        #  <FromUserName>
        #    < ![CDATA[fromUser] ]>
        #  </FromUserName>
        #  <CreateTime>
        #    1348831860
        #  </CreateTime>
        #  <MsgType>
        #    < ![CDATA[text] ]>
        #  </MsgType>
        #  <Content>
        #    < ![CDATA[this is a test] ]>
        #  </Content>
        #  <MsgId>
        #   1234567890123456
        #  </MsgId>
        #</xml>
        #参数            描述
        #ToUserName     开发者微信号
        #FromUserName   发送方帐号（一个OpenID）
        #CreateTime     消息创建时间 （整型）
        #MsgType        text
        #Content        文本消息内容
        #MsgId          消息id，64位整型

        receive = {}
        for i in root:
            receive[i.tag] = i.text
        print(receive['Content'])
        if receive['Content'] == "你好":
            fb_content = feedback_message(receive['FromUserName'], receive['ToUserName'], "你好呀~")
            return fb_content
        if receive['Content'] == "测试课件":
            fb_content = feedback_message(receive['FromUserName'], receive['ToUserName'], "http://mantels.top/wechatcoursewares/id/2/chapter/1/lesson/1")
            return fb_content
        return "success"

#回复文本消息
#范例:
#<xml>
#  <ToUserName>
#    < ![CDATA[toUser] ]>
#  </ToUserName>
#  <FromUserName>
#    < ![CDATA[fromUser] ]>
#  </FromUserName>
#  <CreateTime>
#    12345678
#  </CreateTime>
#  <MsgType>
#    < ![CDATA[text] ]>
#  </MsgType>
#  <Content>
#    < ![CDATA[你好] ]>#
#  </Content>
#</xml>
#参数            是否必须         描述
#ToUserName        是       接收方帐号（收到的OpenID）
#FromUserName      是       开发者微信号
#CreateTime        是       消息创建时间 （整型）
#MsgType           是       text
#Content           是       回复的消息内容（换行：在content中能够换行，微信客户端就支持换行显示）
def feedback_message(ToUserName, FromUserName, Content):
    root = ET.Element("xml")
    subElement(root, "ToUserName", ToUserName)
    subElement(root, "FromUserName", FromUserName)
    subElement(root, "CreateTime", str(int(time())))
    subElement(root, "MsgType", "text")
    subElement(root, "Content", Content)

    tree = ET.ElementTree(root)
    return ET.tostring(root, encoding='utf8')

def subElement(root, tag, text):
    ele = ET.SubElement(root, tag)
    ele.text = text
    ele.tail = '\n'

@wechat.route('/test', methods=['POST', 'GET'])
def test():
    feedback_message("233", "332", "refews")
    return "test"
