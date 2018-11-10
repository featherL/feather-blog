from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from config import config

db = SQLAlchemy()
pagedown = PageDown()


def create_app(config_name):
    """接受配置名作为参数, 创建app实例"""
    app = Flask(__name__)

    # 初始化配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    from .admin import admin as admin_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app
