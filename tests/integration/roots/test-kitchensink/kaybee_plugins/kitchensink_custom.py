"""

Make some custom stuff for testing/demo purposes:

- Custom: resource, widget, reference, genericpage, localtemplates
- Custom: article, article_reference, homepage, section, toctree

"""
from pydantic import BaseModel
from sphinx.application import Sphinx

from kaybee.app import kb
from kaybee.plugins.articles.base_article import BaseArticle
from kaybee.plugins.articles.base_article import BaseArticleModel
from kaybee.plugins.genericpage.genericpage import Genericpage
from kaybee.plugins.resources.base_resource import BaseResource
from kaybee.plugins.widgets.base_widget import (
    BaseWidget,
    BaseWidgetModel,
)


class KsResourceModel(BaseModel):
    ksresource_flag: int


@kb.resource('ksresource')
class KsResource(BaseResource):
    model = KsResourceModel

    @property
    def increment(self):
        return self.props.ksresource_flag + 1


class KsWidgetModel(BaseWidgetModel):
    kswidget_flag: int


@kb.widget('kswidget')
class KsWidget(BaseWidget):
    model = KsWidgetModel

    def make_context(self, context, sphinx_app: Sphinx):
        context['another_flag'] = 835

    @property
    def increment(self):
        return self.props.kswidget_flag + 1


@kb.genericpage()
class KsGenericpage(Genericpage):
    @property
    def increment(self):
        return 9


class KsArticleModel(BaseArticleModel):
    ksarticle_flag: int


@kb.resource('ksarticle')
class KsArticle(BaseArticle):
    model = KsArticleModel

    @property
    def increment(self):
        return self.props.ksarticle_flag + 1
