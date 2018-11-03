from . import main


@main.app_template_filter('md')
def markdown_to_html(content):
    """markdown文本解析"""
    from markdown import markdown
    return markdown(content)
