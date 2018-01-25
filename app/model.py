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

    def __init__(self, number, username, email, password, role, email_check):
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
    setting = db.Column(db.Integer, db.ForeignKey('marksetting.id'))
    chapter = db.relationship('Chapter', backref = 'theclass', lazy = 'dynamic')
    homework = db.relationship('Homework', backref = 'theclass', lazy = 'dynamic')
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
    password = db.Column(db.String(80), unique=False)
    involed_class = db.relationship('Involed_class', backref = 'student', lazy = 'dynamic')
    answer = db.relationship('Answer_Student', backref = 'student', lazy = 'dynamic')

    def __init__(self, number, username, email, password):
        self.number = number
        self.username = username
        self.email = email
        self.password = password

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
