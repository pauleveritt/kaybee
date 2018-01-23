"""

A reference resource based on articles.

"""

from kaybee.plugins.articles.base_article import (
    BaseArticle,
    BaseArticleModel,
)


class BaseArticleReferenceModel(BaseArticleModel):
    label: str


class BaseArticleReference(BaseArticle):
    model = BaseArticleReferenceModel
    is_reference = True
