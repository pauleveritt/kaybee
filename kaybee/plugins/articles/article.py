"""

An out-of-the-box article type.

This can be used in RST with something like::

   .. article::
      template: sometemplate.html

"""

from kaybee.app import kb

from kaybee.plugins.articles.base_article import BaseArticle, BaseArticleModel


@kb.resource('article')
class Article(BaseArticle):
    props: BaseArticleModel
