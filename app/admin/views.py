"""
视图函数
"""

from . import admin
from functools import wraps
from flask import session, g, redirect, url_for, request, render_template, abort
from ..models import User, Article, Tag
from .. import db
from ..forms import ArticleForm


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
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        tags = form.tags.data.split()
        article = Article(title=title, content=content, author=g.user)
        for tag_id in tags:
            tag = Tag.query.filter(Tag.id==tag_id).first()
            if tag:
                article.tags.append(tag)

        session.add(article)
        session.commit()

        return redirect(url_for('main.index'))
    else:
        return render_template('add_article.html', form=form)

