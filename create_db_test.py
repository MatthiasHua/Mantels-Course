import os
from app import db
from app.model import *
from app.modules.coursemanager import *

print("warning: 只用于测试环境,可能会对原数据库造成不可逆破环，请勿在生产环境中使用!")

if not os.path.exists("app\\data"):
    print("未发现data目录")
    os.makedirs("app\\data")
    print("目录创建完成")
if os.path.isfile("app\\data\\data.sqlite"):
    print("已存在数据库是否删除?(y/n)")
    p = input()
    if p == 'y':
        os.remove("app\\data\\data.sqlite")
        print("删除成功！")
    else:
        quit()

print("开始创建测试数据库")
db.create_all()

#默认测试数据

#测试用户
testTeacher = Teacher("123", "123", "123@123.com", "123123", 1, 0)
superMatthias = Teacher("superMatthias", "superMatthias", "superMatthias@123.com", "Matthiassuper", 9, 0)
db.session.add(testTeacher)
db.session.add(superMatthias)

#测试课程
introduction = '''### 使用Markdown
---
- 快速排版
- 多设备显示
- 轻松使用[链接](/)
---

![图片范例](https://gitee.com/Matthias/Mantels-Markdown-Editor/raw/master/img.png)

'''
testClass = new_course("testClass", "1212345", "2018-01-01", "2018-06-30", introduction, 1)

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

#测试学生
testStudent1 = Student("123", "teststudent1", "teststudent1@mantels.top", "123123")
testStudent2 = Student("456", "teststudent2", "teststudent2@mantels.top", "123123")
testStudent3 = Student("789", "zzz","teststudent3@mantels.top", "123123")
db.session.add(testStudent1)
db.session.add(testStudent2)
db.session.add(testStudent3)

#学生2默认选测试课程
testInvoled_class1 = Involed_class(1, 1)
testInvoled_class2 = Involed_class(1, 2)
testInvoled_class3 = Involed_class(1, 3)
db.session.add(testInvoled_class1)
db.session.add(testInvoled_class2)
db.session.add(testInvoled_class3)

#测试习题
body = '''### 测试习题
---
1. 1+1= ~120-提示~

2. 2*3= ~60~

'''
testhomework = Homework(1, 1, "testhomework", body, "2018-1-25", "2018-1-28")
#答案
testanswer = Answer("inputlabel~2~6", 1)
#分值
testscore = Score("0~2~3", 1)
#学生答案
testanswer_student1 = Answer_Student("inputlabel~2~3", 1, 1)
testanswer_student2 = Answer_Student("inputlabel~2~6", 2, 1)
testanswer_student3 = Answer_Student("inputlabel~7~6", 3, 1)

db.session.add(testhomework)
db.session.add(testanswer)
db.session.add(testscore)
db.session.add(testanswer_student1)
db.session.add(testanswer_student2)
db.session.add(testanswer_student3)

db.session.commit()
