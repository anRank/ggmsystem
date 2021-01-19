from flask import Blueprint

web = Blueprint('web', __name__, url_prefix='/')

from app.web import main
from app.web import course
from app.web import teacher
from app.web import graduate
from app.web import t_operation
from app.web import h_operation
from app.web import m_operation