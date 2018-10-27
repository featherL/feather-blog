"""
数据库模型定义
"""

from . import db
from datetime import datetime

# 文章与标签的中间表
article_tag = db.Table(
    'article_tag',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


class User(db.Model):
    """账户"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(50), nullable=False)  # 昵称是公开的
    username = db.Column(db.String(50), nullable=False) # 用户名用于登录，非公开
    password = db.Column(db.String(100), nullable=False)  # 密码hash值


class Article(db.Model):
    """文章"""
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id') )
    author = db.relationship('User', backref=db.backref('articles') )

    tags = db.relationship('Tag', secondary=article_tag, backref=db.backref('articles') )


class Tag(db.Model):
    """文章的标签"""
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(50), nullable=False)



