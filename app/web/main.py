from datetime import timedelta, datetime

from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import desc

from app.web import web
from flask import render_template, request, redirect, url_for, session, current_app
from models.ggm import Manager, Teacher, Graduate, User


@web.route('/')
@login_required
def hello():
    return render_template('test.html')


@web.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        account = request.form.get('account')
        password = request.form.get('password')
    user = User.query.filter_by(account=account, password=password).first()
    login_user(user, remember=True)
    if user.ismanager:
        return redirect(url_for('web.manager_home'))
    elif user.isgraduate:
        return redirect(url_for('web.g_home'))
    elif user.isteacher:
        return redirect(url_for('web.t_home'))


@web.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.login'))