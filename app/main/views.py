"""
视图函数
"""

from . import main


@main.route('/')
def index():
    return '<h1>hello world!</h1>'

