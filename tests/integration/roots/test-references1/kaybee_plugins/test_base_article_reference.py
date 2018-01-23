from kaybee.plugins.articles.base_article_reference import BaseArticleReference


class TestBaseArticleReference:
    def test_import(self):
        assert 'BaseArticleReference' == BaseArticleReference.__name__

    def test_construction(self):
        yaml = """
label: reference1
        """
        bar = BaseArticleReference('somereference1', 'somereference', yaml)
        assert 'reference1' == bar.props.label
