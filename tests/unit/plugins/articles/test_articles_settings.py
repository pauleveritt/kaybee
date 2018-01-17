from kaybee.plugins.articles.settings import ArticlesModel


class TestArticlesSettings:
    def test_import(self):
        assert 'ArticlesModel' == ArticlesModel.__name__

    def test_construction(self):
        am = ArticlesModel(**dict(use_toctree=False))
        assert False is am.use_toctree
