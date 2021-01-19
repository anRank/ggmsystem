from flask import Flask
from flask_cors import CORS
from app.models.base import db
from flask_login import LoginManager


# 创建LoginManager类
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    # 设置允许跨域请求
    CORS(app, supports_credentials=True)

    # 注册蓝图
    from .web import web
    app.register_blueprint(web)

    # 数据库初始化
    db.init_app(app)
    # db.create_all(app=app)

    # 配置login_manager.init_app(app)
    login_manager.init_app(app)
    # 登录视图的名称可以设置为LoginManager.login_view
    login_manager.login_view = 'web.login'
    # 闪烁的默认消息是“要自定义消息”
    login_manager.login_message = '请先登录或注册'
    # with app.app_context():
    #     db.create_all()
    return app
