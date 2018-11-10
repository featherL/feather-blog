"""
数据库模型定义
"""

from . import db
from markdown import markdown
import bleach
from datetime import datetime
from sqlalchemy import event
import hashlib


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

    def set_password(self, password):
        sha1 = hashlib.sha1()
        sha1.update(password.encode('utf-8'))
        hash_code = sha1.hexdigest()
        self.password = hash_code

    def check_password(self, password):
        """校验密码"""
        sha1 = hashlib.sha1()
        sha1.update(password.encode('utf-8'))
        hash_code = sha1.hexdigest()

        return self.password == hash_code


class Article(db.Model):
    """文章"""
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    html_buf = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id') )
    author = db.relationship('User', backref=db.backref('articles') )

    tags = db.relationship('Tag', secondary=article_tag, backref=db.backref('articles') )

    @staticmethod
    def save_to_html(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img']
        target.html_buf = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True)
        )


class Tag(db.Model):
    """文章的标签"""
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(50), nullable=False)


event.listen(Article.content, 'set', Article.save_to_html)



