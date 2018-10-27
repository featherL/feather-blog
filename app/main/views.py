"""
视图函数
"""

from . import main
from flask import render_template, request
from ..models import Article


@main.route('/')
def index():
    page_index = request.args.get('page_index') or 0
    page_count = request.args.get('page_count') or 10

    articles = Article.query.order_by(-Article.create_time).limit(page_count).offset(page_index*page_count).all()

    context = {
        'aritcles':articles
    }

    return render_template('index.html', **context)

