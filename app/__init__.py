from flask import Flask
from config import config

def create_app(config_name):
    """接受配置名作为参数, 创建app实例"""
    app = Flask(__name__)

    # 初始化配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .main import main as main_blueprint
    from .api import api as api_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(api_blueprint, url_prefix='/api')


    return app
