"""
视图函数
"""

from . import admin
from functools import wraps
from flask import session, g, redirect, url_for, render_template, abort
from ..models import User, Article, Tag
from .. import db
from ..forms import ArticleForm, LoginForm
import hashlib


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
    user_id = session.get('user_id')  # 获取账户的id

    g.user = User.query.filter(User.id == user_id).first()


@admin.context_processor
def context_processor():
    return { 'g':g }


@admin.route('/add_article/', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        tags = form.tags.data.split()
        article = Article(title=title, content=content, author=g.user)
        for tag_id in tags:
            tag = Tag.query.filter(Tag.id == tag_id).first()
            if tag:
                article.tags.append(tag)

        db.session.add(article)
        db.session.commit()

        return redirect(url_for('admin.index'))
    else:
        return render_template('add_article.html', form=form)


@admin.route('/')
@login_required
def index():
    return render_template('manage_page.html')


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        sha1 = hashlib.sha1()
        sha1.update(password.encode('utf-8'))
        hash = sha1.hexdigest()

        user = User.query.filter(User.username == username and User.password == hash).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('admin.index'))
        else:
            return render_template('login.html', form=form, errmsg='登录失败')
    else:
        return render_template('login.html', form=form)

