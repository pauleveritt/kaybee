"""

Make some custom stuff for testing/demo purposes:

- Custom: resource, widget, reference, genericpage, localtemplates
- Custom: article, article_reference, homepage, section, toctree

"""

from kaybee.app import kb

from kaybee.plugins.articles.base_article import BaseArticle
from kaybee.plugins.articles.base_article import BaseArticleModel


class KsArticleModel(BaseArticleModel):
    ksarticle_flag: int


@kb.resource('ksarticle')
class KsArticle(BaseArticle):
    model = KsArticleModel

    @property
    def increment(self):
        return self.props.ksarticle_flag + 1
