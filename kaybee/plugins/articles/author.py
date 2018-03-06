from kaybee.app import kb
from kaybee.plugins.articles.base_article_reference import BaseArticleReference


@kb.resource('author')
class Author(BaseArticleReference):
    pass
