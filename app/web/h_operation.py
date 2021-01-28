from flask_login import current_user

from app.web import web
from flask import render_template, request, redirect, url_for

from models.base import db
from models.ggm import Course, Head, Teacher, Subject, Mentor, Graduate, Wish, Activity, Report


# 所负责学科下的课程查看
# 查看学科下导师的研究生情况
@web.route('/head_home')
def head_home():
    # 所负责的学科的id
    my_s_id = Teacher.query.filter_by(name=current_user.username).first().subject.id
    context = {
        # 学科下的课程
        'courses': Course.query.filter_by(subject_id=my_s_id).all(),
        # 学科下的导师
        'mentors': Teacher.query.filter_by(ismentor=1, subject_id=my_s_id).all(),
        'subject': Subject.query.filter_by(id=my_s_id).first()
    }
    return render_template('head/h_home.html', **context)


@web.route('/h_mentor_g/<m_id>')
def h_mentor_g(m_id):
    context = {
        'graduates': Graduate.query.filter_by(mentor_id=m_id).all()
    }
    return render_template('head/h_mentor_gs.html', **context)


@web.route('/set_times', methods=['GET', 'POSt'])
def set_times():
    if request.method == 'GET':
        'post plz'
    else:
        times = request.form.get('times')
    subjects = Subject.query.all()
    teacher = Teacher.query.filter_by(name=current_user.username).first()
    for subject in subjects:
        if subject.name == teacher.subject.name:
            s = subject
    s.c_times = times
    db.session.commit()
    return redirect(url_for('web.head_home'))