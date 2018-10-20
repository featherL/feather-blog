"""
配置文件
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)

    @staticmethod
    def init_app(app):
        pass

class TestingConfig(Config):
    DEBUG = True

config = {
    'testing':TestingConfig
}
