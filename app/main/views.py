"""
视图函数
"""

from . import main
from flask import render_template, request, abort
from ..models import Article


@main.route('/')
def index():
    """首页显示文章列表"""

    page_index = request.args.get('page_index') or 0
    page_count = request.args.get('page_count') or 10

    articles = Article.query.order_by(-Article.create_time).limit(page_count).offset(page_index*page_count).all()

    # print('articles: %s' % articles)  # debug

    context = {
        'articles':articles
    }

    return render_template('index.html', **context)


@main.route('/detail/<article_id>/')
def detail(article_id):
    """文章详情页"""
    article = Article.query.filter(Article.id == article_id).first()
    if article:
        return render_template('detail.html', article=article)
    else:
        abort(404)


