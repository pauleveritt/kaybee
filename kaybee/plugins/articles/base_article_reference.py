"""

A reference resource based on articles.

"""

from kaybee.plugins.references.base_reference import is_reference_target
from kaybee.plugins.articles.base_article import (
    BaseArticle,
    BaseArticleModel,
)


class BaseArticleReferenceModel(BaseArticleModel):
    label: str


class BaseArticleReference(BaseArticle):
    props: BaseArticleReferenceModel
    is_reference = True

    def get_sources(self, resources):
        """ Filter resources based on which have this reference """

        rtype = self.rtype  # E.g. category
        label = self.props.label  # E.g. category1
        result = [
            resource
            for resource in resources.values()
            if is_reference_target(resource, rtype, label)
        ]
        return result
