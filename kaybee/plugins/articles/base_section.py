from kaybee.plugins.articles.base_article import (
    BaseArticle,
    BaseArticleModel,
)


class BaseSectionModel(BaseArticleModel):
    featured_resource: str = None  # docname for this section's feature


class BaseSection(BaseArticle):
    model = BaseSectionModel

    def get_featured_resource(self, resources):
        fr = self.props.featured_resource
        if not fr:
            return None
        else:
            return resources[fr]

    def __json__(self, resources):
        d = super().__json__(resources)
        r = self.get_featured_resource(resources)
        d['get_featured_resource'] = r.docname

        return d
