from app import db

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    email_check = db.Column(db.Integer, unique=False)
    password = db.Column(db.String(80), unique=False)
    role = db.Column(db.Integer, unique=False)
    classpost = db.relationship('Class', backref = 'teacher', lazy = 'dynamic')
    administrator = db.relationship('Administrator', backref = 'teacher', lazy = 'dynamic')

    def __init__(self, number, username, email, password, role, email_check = -1):
        self.number = number
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.email_check = email_check

    def __repr__(self):
        return '<Teacher %r>' % self.username

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursename = db.Column(db.String(80), unique=False)
    courseid = db.Column(db.String(80), unique=False)
    start = db.Column(db.String(40), unique=False)
    end = db.Column(db.String(40), unique=False)
    body = db.Column(db.String(1000), unique=False)
    introduction = db.Column(db.String(1000), unique=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    #setting = db.Column(db.Integer, db.ForeignKey('marksetting.id'))
    chapter = db.relationship('Chapter', backref = 'theclass', lazy = 'dynamic')
    #homework = db.relationship('Homework', backref = 'theclass', lazy = 'dynamic')
    #marksetting = db.relationship('Marksetting', backref = 'theclass', lazy = 'dynamic')
    administrator = db.relationship('Administrator', backref = 'theclass', lazy = 'dynamic')
    involed_class = db.relationship('Involed_class', backref = 'theclass', lazy = 'dynamic')

    def __init__(self, coursename, courseid, start, end, introduction, teacher_id, setting):
        self.coursename = coursename
        self.courseid = courseid
        self.start = start
        self.end = end
        self.introduction = introduction
        self.teacher_id = teacher_id
        self.body = ''
        self.setting = setting

    def __repr__(self):
        return '<Course %r>' % self.coursename

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, unique=False)
    name = db.Column(db.String(80), unique=False)
    introduction = db.Column(db.String(1000), unique=False)
    lesson = db.relationship('Lesson', backref = 'chapter', lazy = 'dynamic')
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    def __init__(self, name, introduction, class_id, index):
        self.name = name
        self.introduction = introduction
        self.class_id = class_id
        self.index = index

    def __repr__(self):
        return '<Chapter %r>' % self.name

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, unique=False)
    name = db.Column(db.String(80), unique=False)
    body = db.Column(db.String(10000), unique=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))

    def __init__(self, name, body, chapter_id, index):
        self.name = name
        self.body = body
        self.chapter_id = chapter_id
        self.index = index

    def __repr__(self):
        return '<Lesson %r>' % self.name

class Administrator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __init__(self, class_id, teacher_id):
        self.teacher_id = teacher_id
        self.class_id = class_id

    def __repr__(self):
        return '<Administrator %r>' % self.class_id

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    email_check = db.Column(db.Integer, unique=False)
    password = db.Column(db.String(80), unique=False)
    involed_class = db.relationship('Involed_class', backref = 'student', lazy = 'dynamic')
    #answer = db.relationship('Answer_Student', backref = 'student', lazy = 'dynamic')

    def __init__(self, number, username, email, password, email_check = -1):
        self.number = number
        self.username = username
        self.email = email
        self.password = password
        self.email_check = email_check

    def __repr__(self):
        return '<Student %r>' % self.username

class Involed_class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __init__(self, class_id, student_id):
        self.class_id = class_id
        self.student_id = student_id

    def __repr__(self):
        return '<Involed_class %r>' % self.class_id

'''
class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, unique=False)
    name = db.Column(db.String(80), unique=False)
    body = db.Column(db.String(10000), unique=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    start = db.Column(db.String(80), unique=False)
    end = db.Column(db.String(80), unique=False)
    answer = db.relationship('Answer', backref = 'homework', lazy = 'dynamic')
    answer_student = db.relationship('Answer_Student', backref = 'homework', lazy = 'dynamic')
    score = db.relationship('Score', backref = 'homework', lazy = 'dynamic')

    def __init__(self, class_id, index, name, body, start, end):
        self.class_id = class_id
        self.index = index
        self.name = name
        self.body = body
        self.start = start
        self.end = end

    def __repr__(self):
        return '<Homework %r>' % self.id

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(10000), unique=False)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'))

    def __init__(self, body, homework_id):
        self.homework_id = homework_id
        self.body = body

    def __repr__(self):
        return '<Answer of Homework %r>' % self.homework_id

class Answer_Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(10000), unique=False)
    student_id =  db.Column(db.Integer, db.ForeignKey('student.id'))
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'))

    def __init__(self, body, student_id, homework_id):
        self.homework_id = homework_id
        self.student_id = student_id
        self.body = body

    def __repr__(self):
        return '<Answer of Homework %r(Student)>' % self.homework_id

#分值表(作业)
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(10000), unique=False)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'))

    def __init__(self, body, homework_id):
        self.homework_id = homework_id
        self.body = body

    def __repr__(self):
        return '<Score of Homework %r>' % self.homework_id

#学生分数（作业)
class Score_Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(10000), unique=False)
    student_id =  db.Column(db.Integer, db.ForeignKey('student.id'))
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'))

    def __init__(self, body, student_id, homework_id):
        self.homework_id = homework_id
        self.student_id = student_id
        self.body = body

    def __repr__(self):
        return '<Score of Homework %r(Student)>' % self.homework_id

#学生课程分数
class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.Integer, unique=False)
    type = db.Column(db.Integer, db.ForeignKey('student.id'))
    student_id =  db.Column(db.Integer, db.ForeignKey('student.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))

    def __init__(self, mark, type, student_id, class_id):
        self.mark = mark
        self.type = type
        self.class_id = class_id
        self.student_id = student_id

    def __repr__(self):
        return '<Mark of Student %r>' % self.student_id

class Marksetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attendance =  db.Column(db.Integer, unique=False)
    homework = db.Column(db.Integer, unique=False)
    examination = db.Column(db.Integer, unique=False)
    total = db.Column(db.Integer, unique=False)
    class_id = db.Column(db.Integer, unique=False)
    #class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    theclass = db.relationship('Class', backref = 'marksetting', lazy = 'dynamic')

    def __init__(self, attendance, homework, examination, total, class_id):
        self.attendance = attendance
        self.homework = homework
        self.examination = examination
        self.total = total
        self.class_id = class_id

    def __repr__(self):
        return '< Mark_Setting of Class %r>' % self.class_id
'''

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    type = db.Column(db.Integer, unique=False)
    score = db.Column(db.Integer, unique=False)
    class_id = db.Column(db.Integer, unique=False)
    start = db.Column(db.String(80), unique=False)
    end = db.Column(db.String(80), unique=False)
    finish_award_rate = db.Column(db.Integer, unique=False)

    def __init__(self, name, type, score, class_id, start, end, finish_award_rate):
        self.name = name
        self.type = type
        self.score = score
        self.class_id = class_id
        self.start = start
        self.end = end
        self.finish_award_rate = finish_award_rate

    def __repr__(self):
        return '< Homework %r>' % self.id

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, unique=False)
    homework_id = db.Column(db.Integer, unique=False)
    type = db.Column(db.Integer, unique=False)
    score = db.Column(db.String(80), unique=False)
    content = db.Column(db.String(80), unique=False)

    def __init__(self, index, homework_id, type, score, content):
        self.index = index
        self.homework_id = homework_id
        self.type = type
        self.score = score
        self.content = content

    def __repr__(self):
        return '< Question %r>' % self.id

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #index = db.Column(db.Inbteger, unique=False)
    question_id = db.Column(db.Integer, unique=False)
    student_id = db.Column(db.Integer, unique=False)
    content = db.Column(db.String(80), unique=False)

    def __init__(self, question_id, student_id, content):
        #self.index = index
        self.question_id = question_id
        self.student_id = student_id
        self.content = content

    def __repr__(self):
        return '< Answer %r>' % self.id

class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, unique=False)
    content = db.Column(db.String(80), unique=False)

    def __init__(self, question_id, content):
        self.question_id = question_id
        self.content = content

    def __repr__(self):
        return '< Answer %r>' % self.id

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, unique=False)
    type = db.Column(db.Integer, unique=False)
    value = db.Column(db.Integer, unique=False)
    student_id = db.Column(db.Integer, unique=False)
    class_id = db.Column(db.Integer, unique=False)

    def __init__(self, index, type, value, student_id, class_id):
        self.index = index
        self.type = type
        self.value = value
        self.student_id = student_id
        self.class_id = class_id

    def __repr__(self):
        return '< Score %r>' % self.id

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    content = db.Column(db.String(80), unique=False)

    def __init__(self, teacher_id, content):
        self.teacher_id = teacher_id
        self.content = content

    def __repr__(self):
        return '< Token of Teacher %r>' % self.teacher_id

class Access_Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    device_name = db.Column(db.String(80), unique=True)
    content = db.Column(db.String(80), unique=False)
    restrict = db.Column(db.String(80), unique=False)
    time = db.Column(db.Integer, unique=False)
    last = db.Column(db.Integer, unique=False)

    def __init__(self, teacher_id, device_name, content, time, last, restrict = "none"):
        self.teacher_id = teacher_id
        self.device_name = device_name
        self.content = content
        self.restrict = restrict
        self.time = time
        self.last = last

    def __repr__(self):
        return '< Access_Key of Teacher %r>' % self.teacher_id

class Student_Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True)
    content = db.Column(db.String(80), unique=False)
    enable = db.Column(db.String(80), unique=False)
    time = db.Column(db.Integer, unique=False)
    last = db.Column(db.Integer, unique=False)

    def __init__(self, student_id, content, enable, time, last):
        self.student_id = student_id
        self.content = content
        self.time = time
        self.last = last
        self.enable = enable

    def __repr__(self):
        return '< Key of Student %r>' % self.student_id

class Email_check_key_teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, unique=True)
    key = db.Column(db.String(80), unique=False)
    time = db.Column(db.Integer, unique=False)

    def __init__(self, teacher_id, key, time):
        self.teacher_id = teacher_id
        self.key = key
        self.time = time

    def __repr__(self):
        return '< Email_check_key of teacher %r>' % self.teacher_id

class Email_check_key_student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True)
    key = db.Column(db.String(80), unique=False)
    time = db.Column(db.Integer, unique=False)

    def __init__(self, student_id, key, time):
        self.student_id = student_id
        self.key = key
        self.time = time

    def __repr__(self):
        return '< Email_check_key of student %r>' % self.student_id

#课程公告
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, unique=False)
    body = db.Column(db.String(10000), unique=False)
    time = db.Column(db.Integer, unique=False)

    def __init__(self, class_id, body, time):
        self.class_id = class_id
        self.body = body
        self.time = time

    def __repr__(self):
        return '< Announcement of Class %r>' % self.class_id

#实验
class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    class_id = db.Column(db.Integer, unique=False)
    teacher_id = db.Column(db.Integer, unique=False)
    guide = db.Column(db.String(10000), unique=False)
    result = db.Column(db.String(10000), unique=False)

    def __init__(self, class_id, teacher_id, name, guide = '', result = ''):
        self.class_id = class_id
        self.guide = guide
        self.name = name
        self.result = result

    def __repr__(self):
        return '< Experiment %r>' % self.id

#实验结果
class ExperimentResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, unique=False)
    device_name = db.Column(db.String(80), unique=False)
    experiment_id = db.Column(db.Integer, unique=False)
    class_id = db.Column(db.Integer, unique=False)
    student_id = db.Column(db.Integer, unique=False)
    content = db.Column(db.String(10000), unique=False)
    time = db.Column(db.Integer, unique=False)


    def __init__(self, index, device_name, experiment_id, class_id, student_id, content, time):
        self.index = index
        self.device_name = device_name
        self.experiment_id = experiment_id
        self.class_id = class_id
        self.student_id = student_id
        self.content = content
        self.time = time

    def __repr__(self):
        return '< ExperimentResult %r>' % self.id

#实验结果_教师测试用
class ExperimentResultteacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, unique=False)
    experiment_id = db.Column(db.Integer, unique=False)
    class_id = db.Column(db.Integer, unique=False)
    teacher_id = db.Column(db.Integer, unique=False)
    content = db.Column(db.String(10000), unique=False)
    time = db.Column(db.Integer, unique=False)


    def __init__(self, index, experiment_id, class_id, teacher_id, content, time):
        self.index = index
        self.experiment_id = experiment_id
        self.class_id = class_id
        self.teacher_id = teacher_id
        self.content = content
        self.time = time

    def __repr__(self):
        return '< ExperimentResult - teacher %r>' % self.id
