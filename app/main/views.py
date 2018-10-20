"""
视图函数
"""

from . import main

@main.route('/')
def hello():
    return '<h1>hello world!</h1>'

