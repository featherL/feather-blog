"""
视图函数
"""

from . import admin
from functools import wraps
from flask import session, g, redirect, url_for, render_template, abort
from ..models import User, Article, Tag
from .. import db
from ..forms import ArticleForm, LoginForm, RegisterForm, TagForm


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
    routes = [  # 所有功能的路由
        ('注销', 'admin.logout'),
        ('创建文章', 'admin.add_article'),
        ('管理标签', 'admin.manage_tags')
    ]
    return { 'g':g, 'routes':routes }


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
    """登录"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter(User.username == username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('admin.index'))
        else:
            return render_template('login.html', form=form, errmsg='登录失败')
    else:
        return render_template('login.html', form=form)


@admin.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect(url_for('admin.login'))


@admin.route('/manage_tags/', methods=['GET', 'POST'])
@login_required
def manage_tags():
    """管理标签"""
    form = TagForm()
    tags = Tag.query.all()
    context = {
        'form':form,
        'tags':tags
    }
    if form.validate_on_submit():
        tag_name = form.tag_name.data
        tag = Tag.query.filter(Tag.tag_name == tag_name).first()
        if tag:
            context['errmsg'] = '标签已存在'
            return render_template('manage_tags.html', **context)
        else:
            tag = Tag(tag_name=tag_name)
            db.session.add(tag)
            db.session.commit()
            return redirect(url_for('admin.manage_tags'))
    else:
        return render_template('manage_tags.html', **context)


@admin.route('/del_tag/<tag_id>/')
@login_required
def del_tag(tag_id):
    """删除标签"""
    tag = Tag.query.filter(Tag.id == tag_id).first()
    if tag:
        db.session.delete(tag)
        db.session.commit()
    return redirect(url_for('admin.manage_tags'))


'''
@admin.route('/register/', methods=['GET', 'POST'])
def register():
    """注册, 注册完毕后注释掉"""
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        nickname = form.nickname.data
        password = form.password.data

        user1 = User.query.filter(User.username == username).first()
        user2 = User.query.filter(User.nickname == nickname).first()
        if user1:
            # 用户名重复
            return render_template('register.html', form=form, errmsg='用户名已存在')
        elif user2:
            # 昵称重复
            return render_template('register.html', form=form, errmsg='昵称已存在')
        else:
            user = User(username=username, nickname=nickname)
            user.set_password(password)  # 加密存储密码

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('admin.login'))
    else:
        return render_template('register.html', form=form)
'''


