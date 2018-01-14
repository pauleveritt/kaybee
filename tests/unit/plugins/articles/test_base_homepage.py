from kaybee.plugins.articles.base_homepage import (
    BaseHomepage,
    BaseHomepageModel,
)


class TestBaseArticle:
    def test_import(self):
        assert 'BaseHomepage' == BaseHomepage.__name__
        assert 'BaseHomepageModel' == BaseHomepageModel.__name__

    def test_construction(self, article_resources):
        homepage = article_resources['index']
        assert 'somelogo.png' == homepage.props.logo
