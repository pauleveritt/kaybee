"""

Make some custom stuff for testing/demo purposes:

- Custom: article_reference, homepage, section

"""
from sphinx.application import Sphinx

from kaybee.app import kb
from kaybee.plugins.articles.base_article import (
    BaseArticle,
    BaseArticleModel,
)
from kaybee.plugins.articles.base_article_reference import (
    BaseArticleReference,
    BaseArticleReferenceModel,
)
from kaybee.plugins.genericpage.genericpage import Genericpage
from kaybee.plugins.resources.base_resource import (
    BaseResource,
    BaseResourceModel
)
from kaybee.plugins.widgets.base_widget import (
    BaseWidget,
    BaseWidgetModel,
)


# Start KsResource Model and Class
class KsResourceModel(BaseResourceModel):
    ksresource_flag: int


@kb.resource('ksresource')
class KsResource(BaseResource):
    props: KsResourceModel

    @property
    def increment(self):
        return self.props.ksresource_flag + 1


# End KsResource Model and Class

class KsWidgetModel(BaseWidgetModel):
    kswidget_flag: int


@kb.widget('kswidget')
class KsWidget(BaseWidget):
    props: KsWidgetModel

    def make_context(self, context, sphinx_app: Sphinx):
        context['another_flag'] = 835

    @property
    def increment(self):
        return self.props.kswidget_flag + 1


@kb.genericpage(order=30)
class KsGenericpage(Genericpage):
    @property
    def increment(self):
        return 9


class KsArticleModel(BaseArticleModel):
    ksarticle_flag: int


@kb.resource('ksarticle')
class KsArticle(BaseArticle):
    props: KsArticleModel

    @property
    def increment(self):
        return self.props.ksarticle_flag + 1


class KsFeatureModel(BaseArticleReferenceModel):
    ksfeature_flag: int


@kb.resource('ksfeature')
class KsFeature(BaseArticleReference):
    props: KsFeatureModel

    @property
    def increment(self):
        return self.props.ksfeature_flag + 1
