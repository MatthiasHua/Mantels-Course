import os
from app import db
from app.model import *

if not os.path.exists("app\\data"):
    print("未发现data目录")
    os.makedirs("app\\data")
    print("目录创建完成")

db.create_all()

#默认测试数据

#测试用户
testTeacher = Teacher("123", "123@123.com", "123123", 1, 0)
db.session.add(testTeacher)

#测试课程
introduction = '''### 使用Markdown
---
- 快速排版
- 多设备显示
- 轻松使用[链接](/)
---

![图片范例](https://github.com/MatthiasHua/Mantels-Markdown-Editor/blob/master/img.png?raw=true)

'''
testClass = Class("testClass", "1212345", "2018-01-01", "2018-06-30", introduction, 1)
db.session.add(testClass)

#测试章节
introduction = '''### 章节预览
---
在这里可以对章节进行概述，或是给出学习该章节时所需要的的参考资料。
'''
testChapter1 = Chapter("The First Chapter", introduction, 1, 1)
testChapter2 = Chapter("The Second Chapter", introduction, 1, 2)
db.session.add(testChapter1)
db.session.add(testChapter2)

#测试Lesson
body = '''### 课件
---
使用课件功能来提供教案，借助markdown语法可以提供文字、图片和表格等多种媒体。同时借助html扩展可以提供音乐和视频等。
'''
testLesson11 = Lesson("1. The First Lesson", body, 1, 1)
testLesson12 = Lesson("2. The Second Lesson", body, 1, 2)
testLesson21 = Lesson("1. The First Lesson",  body, 2, 1)
testLesson22 = Lesson("2. The Second Lesson",  body, 2, 2)
testLesson23 = Lesson("3. The First Lesson",  body, 2, 3)
db.session.add(testLesson11)
db.session.add(testLesson12)
db.session.add(testLesson21)
db.session.add(testLesson22)
db.session.add(testLesson23)

db.session.commit()
