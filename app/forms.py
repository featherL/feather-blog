"""
存储表单类
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class ArticleForm(FlaskForm):
    title = StringField("标题", validators=[DataRequired()])
    tags = StringField("标签", validators=[DataRequired()])
    content = PageDownField("正文", validators=[DataRequired()])
    submit = SubmitField("发布")

