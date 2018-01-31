from kaybee.plugins.articles.base_article import (
    BaseArticle,
    BaseArticleModel,
)


class BaseSectionModel(BaseArticleModel):
    featured_resource: str = None  # docname for this section's feature
    subheading: str = None


class BaseSection(BaseArticle):
    props: BaseSectionModel

    def get_featured_resource(self, resources):
        fr = self.props.featured_resource
        if not fr:
            return None
        else:
            return resources[fr]

    def __json__(self, resources):
        d = super().__json__(resources)
        r = self.get_featured_resource(resources)
        if r:
            d['get_featured_resource'] = r.docname

        return d
