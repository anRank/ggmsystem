from datetime import timedelta, datetime

from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import desc

from app.web import web
from flask import render_template, request, redirect, url_for, session, current_app
from models.ggm import Manager, Teacher, Graduate, User


@web.route('/')
@login_required
def home():
    return render_template('manager/home.html')


@web.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method == 'GET':
    #     return render_template('login.html')
    # else:
    #     id = request.form.get('id')
    #     password = request.form.get('password')
    # user = User.query.filter_by(id=id, password=password).first()
    # login_user(user, remember=True)
    # if user.ismanager:
    #     return redirect(url_for('web.home'))
    # elif user.isgraduate:
    #     return redirect(url_for('web.g_home'))
    # elif user.isteacher:
    #     return redirect(url_for('web.t_home'))
    user = User.query.filter_by(id=1).first()
    login_user(user, remember=True)
    return redirect(url_for('web.home'))


@web.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.login'))