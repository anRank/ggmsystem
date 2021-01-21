from datetime import timedelta, datetime

from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import desc

from app.web import web
from flask import render_template, request, redirect, url_for, session, current_app
from models.ggm import Manager, Teacher, Graduate, User, Subject


@web.route('/m_home')
def manager_home():
    context = {
        'subjects': Subject.query.all()
    }
    return render_template('manager/home.html', **context)