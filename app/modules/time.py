import time, datetime
from app.model import *

#年-月-日
#yyyy-mm-dd
#time.strftime("%Y-%m-%d", time.localtime())

#---------------------------------------
#判断习题状态
#输入
#int: homework_id 作业id
#输出
#int:         result
#     即将开始   1
#     进行中     2
#     批改中     3
#     已结束     4
#---------------------------------------
def check_homework_state(homework_id):
    now = time.strftime("%Y-%m-%d", time.localtime())
    homework = Homework.query.filter_by(id = homework_id).first()
    start = homework.start
    end = homework.end
    print(start, end)
    c = compare_time_day(now, start)
    if c == -1:
        return 1
    if c == 0:
        return 2
    c = compare_time_day(now, end)
    if c <= 0:
        return 2
    #结束日期的后一天的凌晨4点开始进入判题阶段，6点结束
    if compare_time_day_interval(end, now) == 1:
        hour = int(time.strftime("%H", time.localtime()))
        if hour < 4:
            return 2
        if hour < 6:
            return 3
    return 4



#---------------------------------------
#两个日期之间差的天数
#输入
#string: t1,t2 两个日期
#输出
#int: 差的天数
#---------------------------------------
def compare_time_day_interval(t1, t2):
    t1 = datetime.datetime.strptime(t1,'%Y-%M-%d')
    t2 = datetime.datetime.strptime(t2,'%Y-%M-%d')
    return (t2-t1).days

#---------------------------------------
#比较两个日期的大小(日期在后的算大)
#输入
#string: t1,t2 两个日期
#输出
#int:         result
#     t1>t2     1
#     t1=t2     0
#     t1<t2    -1
#---------------------------------------
def compare_time_day(t1, t2):
    t1 = yyyy_mm_dd_to_int(t1)
    t2 = yyyy_mm_dd_to_int(t2)
    if t1 > t2:
        return 1
    if t1 == t2:
        return 0
    if t1 < t2:
        return -1

#---------------------------------------
#yyyy-mm-dd格式日期转yyyymmdd格式数字
#输入
#string: t 日期
#输出
#int: t 日期
#---------------------------------------
def yyyy_mm_dd_to_int(t):
    t = t.split("-")
    return int(t[0]) * 10000 + int(t[1]) * 100 + int(t[2])
