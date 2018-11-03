"""
视图函数
"""

from . import admin
from functools import wraps
from flask import session, g, redirect, url_for, request, render_template, abort
from ..models import User, Article
from .. import db


def login_required(func):
    """做登录限制的装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            abort(403)
    return wrapper


@admin.before_request
def hook_before_request():
    # user_id = session.get('user_id')  # 获取账户的id

    # debug
    user_id = 1
    g.user = User.query.filter(User.id == user_id).first()


@admin.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    if request.method == 'GET':
        return render_template('add_article.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')

        new_article = Article(title=title, content=content)
        new_article.author = g.user

        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('main.index'))



