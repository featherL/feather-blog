"""
存储表单类
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class ArticleForm(FlaskForm):
    """文章的表单"""
    title = StringField("标题", validators=[DataRequired()])
    tags = StringField("标签", validators=[DataRequired()])
    content = PageDownField("正文", validators=[DataRequired()])
    submit = SubmitField("发布")


class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField("用户名", validators=[DataRequired])
    password = PasswordField("密码", validators=[DataRequired])
    submit = SubmitField("登录")



