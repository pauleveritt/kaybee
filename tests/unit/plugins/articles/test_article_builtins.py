from kaybee.plugins.articles.article import Article
from kaybee.plugins.articles.homepage import Homepage
from kaybee.plugins.articles.section import Section


class TestBuiltins:
    def test_imports(self):
        assert 'Article' == Article.__name__
        assert 'Homepage' == Homepage.__name__
        assert 'Section' == Section.__name__
