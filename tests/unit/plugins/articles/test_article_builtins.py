from kaybee.plugins.articles.article import Article
from kaybee.plugins.articles.category import Category
from kaybee.plugins.articles.homepage import Homepage
from kaybee.plugins.articles.section import Section
from kaybee.plugins.articles.toctree import Toctree


class TestBuiltins:
    def test_imports(self):
        assert 'Article' == Article.__name__
        assert 'Category' == Category.__name__
        assert 'Homepage' == Homepage.__name__
        assert 'Section' == Section.__name__
        assert 'Toctree' == Toctree.__name__
