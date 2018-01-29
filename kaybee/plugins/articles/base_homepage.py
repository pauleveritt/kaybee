from kaybee.plugins.articles.base_article import (
    BaseArticle,
    BaseArticleModel
)


class BaseHomepageModel(BaseArticleModel):
    logo: str = None
    heading: str = None
    subheading: str = None
    hero_image: str = None


class BaseHomepage(BaseArticle):
    props: BaseHomepageModel
