from flask_login import current_user

from app.web import web
from flask import render_template, request, redirect, url_for

from models.base import db
from models.ggm import Course, Head, Teacher, Subject, Mentor, Graduate, Wish, Activity, Report


@web.route('/t_home')
def t_home():
    # 确认课程对象的选课对象
    # 展示选择自己所教课程的志愿列表，并进行通过确认
    wishes = []
    for wish in Wish.query.all():
        if wish.course.teacher.name == current_user.username:
            wishes.append(wish)
    courses = []
    for course in Course.query.all():
        if course.teacher.name == current_user.username:
            courses.append(course)
    context = {
        'wishes': wishes,
        'courses': courses
    }
    # 助教工作评价
    return render_template('teacher/t_home.html', **context)


@web.route('/t_wish_pass/<wish_id>')
def t_wish_pass(wish_id):
    # 通过志愿
    wish = Wish.query.filter_by(id=wish_id).first()
    # 如果该助教已被其他课程选定，则不进行改变
    graduate_id = wish.graduate_id
    courses = Course.query.all()
    for course in courses:
        if course.graduate_id == graduate_id:
            # 该助教已经被其他课程选中
            return redirect(url_for('web.t_home'))
    # 进行判断，如果该课程已有助教
    if wish.course.graduate_id is None:
        wish.status = 1
        # 通过一个助教志愿后，该课程将与研究生绑定
        wish.course.graduate_id = wish.graduate_id
        db.session.commit()
        return redirect(url_for('web.t_home'))
    else:
        return redirect(url_for('web.t_home'))


@web.route('/t_course_add_page')
def t_course_add_page():
    return render_template('teacher/t_addcourse.html')


@web.route('/ta_list')
def ta_list():
    # 该老师教授的所有课程
    courses = []
    for course in Course.query.all():
        if course.teacher.name == current_user.username:
            courses.append(course)
    context = {
        'courses': courses
    }
    return render_template('teacher/ta_list.html', **context)