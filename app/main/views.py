"""
视图函数
"""

from . import main
from flask import render_template


@main.route('/')
def index():
    return render_template('index.html')

