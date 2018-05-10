#api
from app.model import *
from app.modules import key
import json
import time

#获取access_key
def get_access_key(data):
    #校验
    result = check_access_key(data)

    if result == 1:
        #生成key
        return create_access_key(data)
    else:
        #返回错误代码
        return result

#获取access_key
def get_access_key_iot(data):
    #校验
    result = check_access_key_iot(data)

    if result == 1:
        #生成key
        return create_access_key_iot(data)
    else:
        #返回错误代码
        return result

def create_access_key(data):
    #获取数据
    number = data.get('number')
    token = data.get('token')
    device_name = data.get('device name')
    lasttime = int(data.get('last time', 7200))

    #生成新的access_key
    accesskey = key.create_key(16)
    try:
        teacher = Teacher.query.filter_by(number = number).first()
        newaccesskey = Access_Key.query.filter_by(teacher_id = teacher.id, device_name = device_name).first()
        #没有旧的key，创建新的key
        if newaccesskey == None:
            print(int(time.time()))
            newaccesskey = Access_Key(teacher.id, device_name, accesskey, int(time.time()), int(time.time()) + lasttime, 'none')
            db.session.add(newaccesskey)
        #有旧的key，更新key
        else:
            newaccesskey.content = accesskey
            newaccesskey.time = int(time.time())
            newaccesskey.last = int(time.time()) + lasttime
        db.session.commit()
    except BaseException as e:
        print(e)
        return "40004"

    #生成返回数据
    verification_code = key.verificate(number + accesskey)
    data = {
        'access_key': accesskey,
        'verification code': verification_code
    }
    data = json.dumps(data)
    data = bytes(data, 'utf8')
    return data

def create_access_key_iot(data):
    #获取数据
    number = data.get('number')
    token = data.get('token')
    device_name = data.get('device name')
    lasttime = int(data.get('last time', 7200))

    #生成新的access_key
    accesskey = key.create_key(16)
    try:
        teacher = Teacher.query.filter_by(number = number).first()
        newaccesskey = Access_Key.query.filter_by(teacher_id = teacher.id, device_name = device_name).first()
        #没有旧的key，创建新的key
        if newaccesskey == None:
            print(int(time.time()))
            newaccesskey = Access_Key(teacher.id, device_name, accesskey, int(time.time()), int(time.time()) + lasttime, 'none')
            db.session.add(newaccesskey)
        #有旧的key，更新key
        else:
            newaccesskey.content = accesskey
            newaccesskey.time = int(time.time())
            newaccesskey.last = int(time.time()) + lasttime
        db.session.commit()
    except BaseException as e:
        print(e)
        return "40004"

    return accesskey


def check_access_key(data):
    #获取数据
    number = data.get('number')
    token = data.get('token')
    device_name = data.get('device name')
    lasttime = int(data.get('last time', 7200))
    verification_code = data.get('verification code')
    #校验
    if key.verificate(number + token + device_name) != verification_code:
        return "40005"
    #有效时间超过上限
    if lasttime > 43200:
        return '40006'
    #不存在的用户
    teacher = Teacher.query.filter_by(number = number).first()
    if teacher == None:
        return '40001'
    #当前用户没有打开令牌功能
    token_db = Token.query.filter_by(teacher_id = teacher.id).first()
    if token_db == None:
        return '40002'
    #token错误
    if token_db.content != token:
        return '40003'
    return 1

def check_access_key_iot(data):
    #获取数据
    number = data.get('number')
    token = data.get('token')
    device_name = data.get('device name')
    lasttime = int(data.get('last time', 7200))
    #有效时间超过上限
    if lasttime > 43200:
        return '40006'
    #不存在的用户
    teacher = Teacher.query.filter_by(number = number).first()
    if teacher == None:
        return '40001'
    #当前用户没有打开令牌功能
    token_db = Token.query.filter_by(teacher_id = teacher.id).first()
    if token_db == None:
        return '40002'
    #token错误
    if token_db.content != token:
        return '40003'
    return 1
