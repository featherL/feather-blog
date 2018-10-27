"""
错误处理页面
"""

from . import admin
from flask import render_template


@admin.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404