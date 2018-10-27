from . import api
from flask import request, jsonify
from .api_raw import get_articles


@api.route('/get_articles', methods=['POST'])
def api_get_articles():
    """获取最新的几篇文章"""
    limit = request.form.get('limit')
    offset = request.form.get('offset')

    # debug
    # print('limit={}, offset={}'.format(limit, offset))

    return jsonify({'article': get_articles(limit, offset)})
