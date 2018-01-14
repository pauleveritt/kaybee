from kaybee.plugins.articles.base_article import (
    BaseArticle,
    BaseArticleModel,
)


class BaseSectionModel(BaseArticleModel):
    pass


class BaseSection(BaseArticle):
    model = BaseSectionModel
    toctree = []