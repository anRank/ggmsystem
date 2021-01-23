from datetime import timedelta, datetime

from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import desc

from app.web import web
from flask import render_template, request, redirect, url_for, session, current_app

from models.base import db
from models.ggm import Manager, Teacher, Graduate, User, Subject


@web.route('/m_home')
def manager_home():
    context = {
        'subjects': Subject.query.all()
    }
    return render_template('manager/home.html', **context)


@web.route('/add_manager', methods=['GET', 'POST'])
def add_manager():
    if request.method == 'GET':
        return 'post plz'
    else:
        account = request.form.get('account')
        username = request.form.get('username')
        password = request.form.get('password')
    user = User(account=account, username=username, password=password, isgraduate=0, isteacher=0, ismanager=1,
                ismentor=0, ishead=0)
    db.session.add(user)
    db.session.commit()
    return render_template('login.html')