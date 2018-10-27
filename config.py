"""
配置文件
"""

import os

HOSTNAME = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = 'flask_test'
DATABASE = 'feather_blog'
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME, PASSWORD,
                                                              HOSTNAME, PORT, DATABASE)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True  # debug模式
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or DB_URI


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or DB_URI


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or DB_URI


config = {
    'development': DevelopmentConfig,
    'testing':TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
