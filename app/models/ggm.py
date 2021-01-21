from app import login_manager
from models.base import db
from flask_login import UserMixin
from datetime import datetime, date


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(20))
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    isgraduate = db.Column(db.Integer)
    isteacher = db.Column(db.Integer)
    ismanager = db.Column(db.Integer)
    ismentor = db.Column(db.Integer)
    ishead = db.Column(db.Integer)


# 需要提供一个user_loader回调。此回调用于从会话中存储的用户ID重新加载用户对象。它应该unicode带有用户的ID，并返回相应的用户对象:
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))


class Graduate(UserMixin, db.Model):
    __tablename__ = 'graduate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    cardid = db.Column(db.String(50))
    sex = db.Column(db.Integer)
    birth = db.Column(db.DATE)
    admissiondate = db.Column(db.DATE, default=datetime.now)
    email = db.Column(db.String(100))
    tele = db.Column(db.String(20))
    password = db.Column(db.String(50))
    # 参与项目的id
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', backref=db.backref('graduate'))
    # 导师的id
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))
    mentor = db.relationship('Mentor', backref=db.backref('graduates'))


class Teacher(UserMixin, db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    worknum = db.Column(db.String(50))
    sex = db.Column(db.Integer)
    birth = db.Column(db.DATE)
    email = db.Column(db.String(100))
    tele = db.Column(db.String(20))
    password = db.Column(db.String(50))
    ismentor = db.Column(db.Integer)
    ishead = db.Column(db.Integer)
    # 所属学科的ids
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship('Subject', backref=db.backref('teachers'))


class Head(db.Model):
    __tablename__ = 'head'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 授课教师的id
    hteacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    who = db.relationship('Teacher', backref=db.backref('head'))


class Mentor(db.Model):
    __tablename__ = 'mentor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 授课教师的id
    mteacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    who = db.relationship('Teacher', backref=db.backref('mentor'))


class Manager(UserMixin, db.Model):
    __tablename__ = 'manager'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    workid = db.Column(db.String(50))
    password = db.Column(db.String(50))


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    number = db.Column(db.String(50))
    hours = db.Column(db.Integer)
    type = db.Column(db.Integer)
    selected_num = db.Column(db.Integer)
    start_date = db.Column(db.DATE, default=datetime.now)
    start_term = db.Column(db.DATE, default=datetime.now)
    # 课程优先级
    priority = db.Column(db.Integer, default=0)
    # 授课教师的id
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship('Teacher', backref=db.backref('course'))
    # 所属学科的id
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship('Subject', backref=db.backref('course'))
    # 助教的id
    graduate_id = db.Column(db.Integer, db.ForeignKey('graduate.id'))
    graduate = db.relationship('Graduate', backref=db.backref('course'))


class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    intro = db.Column(db.TEXT)
    # 要求交流次数
    c_times = db.Column(db.Integer)


class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String(100))
    e_name = db.Column(db.String(100))
    intro = db.Column(db.TEXT)
    attachment = db.Column(db.String(100))
    status = db.Column(db.Integer)
    mentor_time = db.Column(db.DateTime, default=datetime.now)
    collge_time = db.Column(db.DateTime, default=datetime.now)
    # 所属活动的id
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    activity = db.relationship('Activity', backref=db.backref('reports'))
    # 提交的研究生的id
    graduate_id = db.Column(db.Integer, db.ForeignKey('graduate.id'))
    graduate = db.relationship('Graduate', backref=db.backref('reports'))


class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    country = db.Column(db.String(50))
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    time = db.Column(db.DATE, default=datetime.now)


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    start_date = db.Column(db.DATE)
    end_date = db.Column(db.DATE)
    name = db.Column(db.String(100))
    funds = db.Column(db.DECIMAL(8, 2))
    status = db.Column(db.Integer)
    approval_time = db.Column(db.DateTime, default=datetime.now)
    # 负责人的id，这里的负责人是Teacher
    pteacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship('Teacher', backref=db.backref('projects'))


class Wish(db.Model):
    __tablename__ = 'wish'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wish_n = db.Column(db.Integer)
    status = db.Column(db.Integer)
    # ispass = db.Column(db.Integer)
    # 研究生的id
    graduate_id = db.Column(db.Integer, db.ForeignKey('graduate.id'))
    graduate = db.relationship('Graduate', backref=db.backref('wish'))
    # 课程的id
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', backref=db.backref('wishes'))


class Evaluation(db.Model):
    __tablename__ = 'evaluation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 评价内容
    content = db.Column(db.String(200))
    # 研究生的id
    graduate_id = db.Column(db.Integer, db.ForeignKey('graduate.id'))
    graduate = db.relationship('Graduate', backref=db.backref('evaluation'))
    # 评价教师的id
    eteacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship('Teacher', backref=db.backref('teacher'))