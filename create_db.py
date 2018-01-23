import os
from app import db
from app.model import *

if not os.path.exists("app\\data"):
    print("未发现data目录")
    os.makedirs("app\\data")
    print("目录创建完成")

if os.path.isfile("app\\data\\data.sqlite"):
    print("已存在数据库是否删除?(y/n)")
    p = input()
    if p == 'y':
        print("危险!请再次确认是否删除数据库?(yes/no)")
        p = input()
        if p == 'yes':
            os.remove("app\\data\\data.sqlite")
            print("删除成功！")
        else:
            quit()
    else:
        quit()

db.create_all()
