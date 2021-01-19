from flask_login import current_user

from app.web import web
from flask import render_template, request, redirect, url_for

from models.base import db
from models.ggm import Course, Head, Teacher, Subject, Mentor, Graduate, Wish, Activity, Report


@web.route('/graduate_list')
def graduate_list():
    context = {
        'graduates': Graduate.query.all()
    }
    return render_template('manager/graduate/graduate.html', **context)


@web.route('/graduate_add_page')
def graduate_add_page():
    return render_template('manager/graduate/addgraduate.html')


@web.route('/graduate_add', methods=['GET', 'POST'])
def graduate_add():
    if request.method == 'GET':
        'post pls'
    else:
        name = request.form.get('name')
        cardid = request.form.get('cardid')
        sex = request.form.get('sex')
        birth = request.form.get('birth')
        admissiondate = request.form.get('admissiondate')
        email = request.form.get('email')
        tele = request.form.get('start_date')
        mentor = request.form.get('mentor')

    mentor_id = Teacher.query.filter_by(name=mentor).first().mentor[0].id
    graduate = Graduate(name=name, cardid=cardid, birth=birth, admissiondate=admissiondate, sex=sex, email=email,
                        tele=tele,
                        mentor_id=mentor_id)
    db.session.add(graduate)
    db.session.commit()
    return redirect(url_for('web.graduate_list'))


@web.route('/g_home')
def g_home():
    username = current_user.username
    id = Graduate.query.filter_by(name=username).first().id
    context = {
        'wishes': Wish.query.filter_by(graduate_id=id).all(),
        'reports': Report.query.filter_by(graduate_id=id).all()
    }
    return render_template('graduate/g_home.html', **context)


@web.route('/g_wish_commit', methods=['GET', 'POST'])
def g_wish_commit():
    if request.method == 'GET':
        return 'post plz'
    else:
        username = request.form.get('username')
        course_id = request.form.get('course_id')
        wish_n = request.form.get('wish')
    graduate = Graduate.query.filter_by(name=username).first()
    wish = Wish(wish_n=wish_n, graduate_id=graduate.id, course_id=course_id)
    db.session.add(wish)
    db.session.commit()
    return redirect(url_for('web.g_home'))


@web.route('/g_report')
def g_report():
    return render_template('graduate/g_report.html')


@web.route('/g_report_commit', methods=['GET', 'POST'])
def g_report_commit():
    if request.method == 'GET':
        return 'post plz'
    else:
        activity_name = request.form.get('activity')
        c_name = request.form.get('c_name')
        e_name = request.form.get('e_name')
        intro = request.form.get('intro')
        attachment = request.form.get('attachment')
    graduate = Graduate.query.filter_by(name=current_user.username).first()
    activity_id = Activity.query.filter_by(name=activity_name).first().id
    report = Report(c_name=c_name, e_name=e_name, intro=intro, attachment=attachment, activity_id=activity_id,
                    graduate_id=graduate.id)
    db.session.add(report)
    db.session.commit()
    return redirect(url_for('web.g_home'))