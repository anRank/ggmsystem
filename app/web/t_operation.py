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
        if wish.course.teacher_id == current_user.id:
            wishes.append(wish)
    context = {
        'wishes': wishes
    }
    # 助教工作评价
    return render_template('teacher/t_home.html', **context)


@web.route('/t_wish_pass/<wish_id>')
def t_wish_pass(wish_id):
    wish = Wish.query.filter_by(id=wish_id).first()
    wish.status = 1
    db.session.commit()
    return redirect(url_for('web.t_home'))


@web.route('/t_course_add_page')
def t_course_add_page():
    return render_template('teacher/t_addcourse.html')