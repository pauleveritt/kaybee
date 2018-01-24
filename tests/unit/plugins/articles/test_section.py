import pytest

from kaybee.plugins.articles.section import Section


@pytest.fixture()
def dummy_section():
    yaml = """
featured_resource: f1/about    
    """
    yield Section('section1', 'section', yaml)


class TestSection:
    def test_import(self):
        assert 'Section' == Section.__name__

    def test_construction(self, dummy_section):
        assert 'f1/about' == dummy_section.props.featured_resource

    def test_no_featured_resource(self, dummy_section, article_resources):
        dummy_section.props.featured_resource = None
        result = dummy_section.featured_resource(article_resources)
        assert None is result

    def test_featured_resource(self, dummy_section, article_resources):
        result = dummy_section.featured_resource(article_resources)
        assert 'f1/about' == result.docname
