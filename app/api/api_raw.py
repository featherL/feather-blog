"""
数据库操作的一些api
"""

from ..models import Article


def get_articles(limit, offset):
    """
    从数据库中获取多篇最新文章
    :param limit:  一次取出的数量
    :param offset:  偏移
    :return:  返回Article实例的列表
    """
    try:
        limit = int(limit)
        offset = int(offset)
        if limit > 0 and offset >= 0:
            return Article.query.all().order_by(-Article.create_time).limit(limit).offset(offset*limit).items
        else:
            raise ValueError
    except (ValueError, TypeError):
        return []


