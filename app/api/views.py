from . import api
from flask import request, jsonify
from .api_raw import get_articles


@api.route('/get_articles', methods=['POST'])
def get_articles():
    """获取最新的几篇文章"""
    limit = int(request.form['limit'])
    offset = int(request.form['offset'])
    return jsonify({'article': get_articles(limit, offset)})


