#成绩相关操作库

from app.model import *
from app import db

#---------------------------------------
# setting课程成绩设置
#given: 是否给定成绩设定(0为未给, 1为给定)
#attendance
#homework
#examination
#total
#sum: attendance + homework + examination
#homework_full_mark: 作业的总分（实际满分）
#---------------------------------------

#---------------------------------------
#计算学生在一门课程中的总分，在数据库中更新，并返回
#输入:
#int: student_id 学生id
#int: class_id 课程id
#int: sub(可选) 是否重新计算分项小分（0为不计算, 1为计算） 默认为0
#dict: setting(可选) 课程成绩设置 setting ['given'] 是否给定成绩设定(0为未给, 1为给定) 默认为0
#输出:
#int: mark 总分
#---------------------------------------
def update_mark_student_total(student_id, class_id, sub = 0, setting = {'given': 0}):
    #存放总成绩
    mark = 0
    #存放平时成绩
    mark_attendance = 0
    #存放线上成绩
    mark_homework = 0
    #存放线下成绩
    mark_examination = 0
    #未给定设定时读取设定
    if setting['given'] == 0:
        setting = get_setting(class_id, setting)
    #重新计算小分
    if sub == 1:
        update_mark_student_homework(student_id, class_id)
    #获取所有成绩
    mark_all = Mark.query.filter_by(student_id = student_id, class_id = class_id).all()
    #处理每一个成绩
    for i in mark_all:
        #不处理type为total的成绩(总成绩)
        if i.type == 'attendance':
            mark_attendance += i.mark
        if i.type == 'homework':
            mark_homework += i.mark
        #应该用startwith
        if i.type == 'examination':
            mark_examination += i.mark
    if setting['attendance'] != 0:
        mark += float(mark_attendance)*setting['total']/setting['sum']
    if setting['homework'] != 0:
        mark += float(mark_homework)*setting['total']*setting['homework']/setting['sum']/setting['homework_full_mark']
    if setting['examination'] != 0:
        mark += float(mark_examination)*setting['total']/setting['sum']
    mark = round(mark)
    mark_total = Mark.query.filter_by(student_id = student_id, class_id = class_id, type = 'total').all()
    if mark_total == []:
        mark_total = Mark(mark, 'total', student_id, class_id)
        db.session.add(mark_total)
    else:
        mark_total[0].mark = mark
    db.session.commit()
    return mark

#---------------------------------------
#计算某一门课程中所有学生的总分，在数据库中更新并返回
#输入:
#int: class_id 课程id
#int: sub(可选) 是否重新计算分项小分（0为不计算, 1为计算）
#输出
#list: 分数列表 list中的每一项为一个list，包括了一个学生的分数信息
#      number:学号
#      username: 姓名
#      mark: 成绩
#---------------------------------------
def update_mark_class_total(class_id, sub = 0):
    setting = get_setting(class_id, {'given': '1'})
    involed_class = Involed_class.query.filter_by(class_id = class_id).all()
    mark_list = []
    for i in involed_class:
        mark = update_mark_student_total(i.student_id, class_id, sub, setting)
        mark_list.append((i.student.number, i.student.username, mark))
    return mark_list

#---------------------------------------
#计算学生在一门课程中的作业总分，在数据库中更新并返回
#输入:
#int: student_id 学生id
#int: class_id 课程id
#输出:
#int: mark 分数
#---------------------------------------
def update_mark_student_homework(student_id, class_id):
    mark = 0
    homeworks = Homework.query.filter_by(class_id = class_id).all()
    for i in homeworks:
        #成绩（带小分）
        r = Score_Student.query.filter_by(student_id = student_id, homework_id = i.id).all()
        if r != []:
            r = r[0].body.split('~')
            mark += int(r[len(r) - 1])
    mark_db = Mark.query.filter_by(student_id = student_id, class_id = class_id, type = 'homework').all()
    if mark_db == []:
        mark_db = Mark(mark, 'homework', student_id, class_id)
        db.session.add(mark_db)
    else:
        mark_db[0].mark = mark
    db.session.commit()
    return mark

#---------------------------------------
#对作业进行自动批改, 在数据库中更新并返回
#输入:
#int: id 作业(Answer_Student)的id
#输出:
#int: 成功时返回 mark 分数
#     失败时返回原因:
#     -1: 没有当前id的作业
#---------------------------------------
def judge_homework_by_answer_student_id(id):
    answer_student = Answer_Student.query.filter_by(id = id).all()
    #没找到
    if answer_student == []:
        return -1
    #批改结果
    result = ''
    sum = 0
    #作业(Homework)的id
    homework_id = answer_student[0].homework_id
    #标准答案
    answer = Answer.query.filter_by(homework_id = homework_id).first()
    #分值
    score = Score.query.filter_by(homework_id = homework_id).first()

    answer_list = answer.body.split('~')
    #学生答案
    answer_student_list = answer_student[0].body.split('~')
    score_list = score.body.split('~')

    for index, a in enumerate(answer_student_list):
        if a == answer_list[index]:
            result += score_list[index]+'~'
            sum += int(score_list[index])
        else:
            result += '0~'
    result += str(sum)
    #检查是否已经批改过
    old_score_student = Score_Student.query.filter_by(homework_id = homework_id, student_id = answer_student[0].student_id).all()
    #批改过的情况下更新成绩
    if old_score_student != []:
        old_score_student[0].body = result
    #未批改过则写入成绩
    else:
        score_student = Score_Student(result, answer_student[0].student_id, homework_id)
        db.session.add(score_student)
    db.session.commit()
    return sum

#---------------------------------------
#通过class_id读取课程中作业的总分（实际满分）,并返回
#输入:
#int: class_id 课程id
#输出:
#int: mark 总分
#---------------------------------------
def get_homework_full_mark(class_id):
    mark = 0
    scorelist = []
    homeworklist = Homework.query.filter_by(class_id = class_id).all()
    for i in homeworklist:
        s = Score.query.filter_by(homework_id = i.id).first()
        if s != None:
            scorelist.append(Score.query.filter_by(homework_id = i.id).first())
    for i in scorelist:
        for j in i.body.split('~'):
            mark += int(j)
    return mark

#---------------------------------------
#通过class_id读取成绩设定
#输入:
#int: class_id 课程id
#输出:
#list: setting 设定
#---------------------------------------
def get_setting(class_id, setting = {'given': 1}):
    rs = Marksetting.query.filter_by(class_id = class_id).first()
    setting['attendance'] = rs.attendance
    setting['homework'] = rs.homework
    setting['examination'] = rs.examination
    setting['total'] = rs.total
    setting['homework_full_mark'] = get_homework_full_mark(class_id)
    #三项成绩和
    setting['sum'] = setting['attendance'] + setting['homework'] + setting['examination']
    #检查设定
    if setting['total'] == 0:
        total = setting['sum']
    return setting

#---------------------------------------
#获取最后一个成绩(总成绩)
#输入:
#string body 成绩信息
#输出:
#int: mark 成绩
#---------------------------------------
def score_list_to_full_mark(body):
    body_list = body.split("~")
    return int(body_list[len(body_list) - 1])

def update_homework_scoce(homework, student_id, class_id):
    val = 0
    questions = Question.query.filter_by(homework_id = homework.id).all()
    for q in questions:
        answer = Answer.query.filter_by(question_id = q.id, student_id = student_id).first()
        solution = Solution.query.filter_by(question_id = q.id).first()
        if answer != None and solution != None and answer.content == solution.content:
            val += int(q.score)
    oldscore = Score.query.filter_by(type = "homework", student_id = student_id, class_id = class_id, index = homework.id).first()
    if oldscore == None:
        score = Score(homework.id, "homework", val, student_id, homework.id)
        db.session.add(score)
    else:
        oldscore.value = val
    db.session.commit()
    pass
