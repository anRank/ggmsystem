from flask_login import current_user

from app.web import web
from flask import render_template, request, redirect, url_for

from models.base import db
from models.ggm import Course, Head, Teacher, Subject, Mentor, Graduate, Wish, Activity, Report


@web.route('/mentor_home')
def mentor_home():
    # 审核通过学术交流情况报告
    # 展示选择自己所教课程的志愿列表，并进行通过确认
    my_id = Teacher.query.filter_by(name=current_user.username).first().id
    # print(Graduate.query.filter_by(mentor_id=my_id).first().name)
    print(123)
    context = {
        'graduates': Graduate.query.filter_by(mentor_id=my_id).all()
    }
    return render_template('mentor/m_home.html', **context)


@web.route('/view_report/<g_id>/')
def view_report(g_id):
    context = {
        'reports': Report.query.filter_by(graduate_id=g_id).all()
    }
    return render_template('mentor/report_view.html', **context)


@web.route('/pass_report/<g_id>/<r_id>')
def pass_report(g_id, r_id):
    report = Report.query.filter_by(id=r_id).first()
    report.status = 1
    db.session.commit()
    return redirect(url_for('web.view_report', g_id=g_id))
