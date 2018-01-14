from kaybee.plugins.articles.base_toctree import BaseToctree


class TestBaseToctree:
    def test_import(self):
        assert 'BaseToctree' == BaseToctree.__name__

