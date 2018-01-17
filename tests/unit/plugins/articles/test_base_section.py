from kaybee.plugins.articles.base_section import (
    BaseSection,
    BaseSectionModel,
)


class TestBaseSection:
    def test_import(self):
        assert 'BaseSection' == BaseSection.__name__
        assert 'BaseSectionModel' == BaseSectionModel.__name__

    def test_section_f1(self, article_resources):
        a = BaseSection('f1/f2/f3/another', 'rtype', '')
        result = a.section(article_resources)
        assert 'f1/f2/f3/index' == result.docname

    def test_featured_resource(self, article_resources):
        f1: BaseSection = article_resources['f1/index']
        result = f1.get_featured_resource(article_resources)
        featured = article_resources['f1/f2/about']
        assert featured == result

    def test_nofeatured_resource(self, article_resources):
        # Remove the prop
        f1: BaseSection = article_resources['f1/index']
        f1.props.featured_resource = None
        result = f1.get_featured_resource(article_resources)
        assert None is result

    def test_to_json(self, article_resources):
        f1 = article_resources['f1/index']
        result = f1.__json__(article_resources)['get_featured_resource']
        assert 'f1/f2/about' == result
