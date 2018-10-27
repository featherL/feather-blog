"""
视图函数
"""

from . import main
from flask import render_template


@main.route('/')
def index():
    return '<h1>hello world!</h1>'

