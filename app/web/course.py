from datetime import timedelta

from flask_login import login_required, login_user, current_user
from sqlalchemy import desc

from app.web import web
from flask import render_template, request, redirect, url_for, session

from models.base import db
from models.ggm import Course, Head, Teacher, Subject, Manager


@web.route('/course_list')
def course_list():
    context = {
        'courses': Course.query.all()
    }
    return render_template('manager/course/course.html', **context)


@web.route('/course_add_page')
def course_add_page():
    return render_template('manager/course/addcourse.html')


@web.route('/course_add', methods=['GET', 'POST'])
def course_add():
    if request.method == 'GET':
        'post pls'
    else:
        name = request.form.get('name')
        number = request.form.get('number')
        hours = request.form.get('hours')
        type = request.form.get('type')
        selected_number = request.form.get('selected_number')
        start_date = request.form.get('start_date')
        teacher = request.form.get('teacher')
        subject = request.form.get('subject')
    teacher_id = Teacher.query.filter_by(name=teacher).first().id
    subject_id = Subject.query.filter_by(name=subject).first().id
    course = Course(name=name, number=number, hours=hours, type=type, selected_num=selected_number, start_date=start_date,
                    teacher_id=teacher_id, subject_id=subject_id)
    db.session.add(course)
    db.session.commit()
    return redirect(url_for('web.course_list'))


@web.route('/clist_for_g')
def clist_for_g():
    context = {
        'courses': Course.query.all()
    }
    return render_template('graduate/g_course.html', **context)