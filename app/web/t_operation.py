from flask_login import current_user

from app.web import web
from flask import render_template, request, redirect, url_for

from models.base import db
from models.ggm import Course, Head, Teacher, Subject, Mentor, Graduate, Wish, Activity, Report, Evaluation, Project


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
    projects = []
    for project in Project.query.all():
        if project.teacher.name == current_user.username:
            projects.append(project)
    context = {
        'wishes': wishes,
        'courses': courses,
        'projects': projects
    }
    # 助教工作评价
    print(321)
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


@web.route('/t_evaluate', methods=['GET', 'POST'])
def t_evaluate():
    if request.method == 'GET':
        return 'post plz'
    else:
        graduate_id = request.form.get('graduate_id')
        content = request.form.get('content')
    teacher = Teacher.query.filter_by(worknum=current_user.account).first()
    evaluation = Evaluation(content=content, graduate_id=graduate_id, eteacher_id=teacher.id)
    db.session.add(evaluation)
    db.session.commit()
    return redirect(url_for('web.ta_list'))


@web.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'GET':
        return 'post plz'
    else:
        name = request.form.get('name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        funds = request.form.get('funds')
    teacher = Teacher.query.filter_by(worknum=current_user.account).first()
    project = Project(start_date=start_date, end_date=end_date, name=name, funds=funds, status=0, pteacher_id=teacher.id)
    db.session.add(project)
    db.session.commit()
    return redirect(url_for('web.t_home'))


@web.route('/project_detail/<id>')
def project_detail(id):
    project = Project.query.filter_by(id=id).first()
    graduates = Graduate.query.filter_by(project_id=id).all()
    context = {
        'project': project,
        'graduates': graduates
    }
    return render_template('teacher/project_detail.html', **context)


@web.route('/project_add_g/<id>', methods=['GET', 'POST'])
def project_add_g(id):
    if request.method == 'GET':
        return 'post plz'
    else:
        name = request.form.get('name')
        cardid = request.form.get('cardid')
    graduate = Graduate.query.filter_by(name=name, cardid=cardid).first()
    graduate.project_id = id
    db.session.commit()
    return redirect(url_for('web.project_detail', id=id))