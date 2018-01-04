from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    email_check = db.Column(db.Integer, unique=False)
    password = db.Column(db.String(80), unique=False)
    role = db.Column(db.Integer, unique=False)
    classpost = db.relationship('Class', backref = 'teacher', lazy = 'dynamic')
    administrator = db.relationship('Administrator', backref = 'teacher', lazy = 'dynamic')

    def __init__(self, username, email, password, role, email_check):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.email_check = email_check

    def __repr__(self):
        return '<User %r>' % self.username

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursename = db.Column(db.String(80), unique=False)
    courseid = db.Column(db.String(80), unique=False)
    start = db.Column(db.String(40), unique=False)
    end = db.Column(db.String(40), unique=False)
    introduction = db.Column(db.String(1000), unique=False)
    body = db.Column(db.String(1000), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chapter = db.relationship('Chapter', backref = 'class', lazy = 'dynamic')
    administrator = db.relationship('Administrator', backref = 'class', lazy = 'dynamic')
    involed_class = db.relationship('Involed_class', backref = 'class', lazy = 'dynamic')

    def __init__(self, coursename, courseid, start, end, introduction, user_id):
        self.coursename = coursename
        self.courseid = courseid
        self.start = start
        self.end = end
        self.introduction = introduction
        self.user_id = user_id
        self.body = ''

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, class_id, user_id):
        self.user_id = user_id
        self.class_id = class_id

    def __repr__(self):
        return '<Administrator %r>' % self.class_id

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), unique=False)
    involed_class = db.relationship('Involed_class', backref = 'student', lazy = 'dynamic')

    def __init__(self, username, email, password):
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
