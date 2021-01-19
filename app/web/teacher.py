from app.web import web
from flask import render_template, request, redirect, url_for

from models.base import db
from models.ggm import Course, Head, Teacher, Subject, Mentor, User


@web.route('/teacher_list')
def teacher_list():
    context = {
        'teachers': Teacher.query.all()
    }
    return render_template('manager/teacher/teacher.html', **context)


@web.route('/teacher_add_page')
def teacher_add_page():
    return render_template('manager/teacher/addteacher.html')


@web.route('/teacher_add', methods=['GET', 'POST'])
def teacher_add():
    if request.method == 'GET':
        'post pls'
    else:
        name = request.form.get('name')
        worknum = request.form.get('worknum')
        birth = request.form.get('birth')
        sex = request.form.get('sex')
        email = request.form.get('email')
        tele = request.form.get('tele')
        ismentor = request.form.get('ismentor')
        ishead = request.form.get('ishead')
        subject = request.form.get('subject')

    subject_id = Subject.query.filter_by(name=subject).first().id
    teacher = Teacher(name=name, worknum=worknum, birth=birth, sex=sex, email=email, tele=tele,
                      ismentor=ismentor, ishead=ishead, subject_id=subject_id)
    db.session.add(teacher)
    db.session.commit()
    t_id = Teacher.query.filter_by(worknum=worknum).first().id
    if ishead:
        head = Head(hteacher_id=t_id)
        db.session.add(head)
    if ismentor:
        mentor = Mentor(mteacher_id=t_id)
        db.session.add(mentor)
    user = User(username=name, account=worknum, password=0, isgraduate=0, isteacher=1, ismanager=0, ismentor=ismentor, ishead=ishead)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('web.teacher_list'))


@web.route('/mentor_list')
def mentor_list():
    context = {
        'mentors': Mentor.query.all()
    }
    return render_template('manager/teacher/mentor.html', **context)


@web.route('/head_list')
def head_list():
    context = {
        'heads': Head.query.all()
    }
    return render_template('manager/teacher/head.html', **context)