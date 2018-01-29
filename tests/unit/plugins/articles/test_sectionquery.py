import pytest
from kaybee.plugins.articles.sectionquery import SectionqueryWidget


@pytest.fixture()
def dummy_sectionquery():
    yaml = """
    name: w23
    query:
      rtype: section
      limit: 5        
    """
    qlw = SectionqueryWidget('widget1', 'widget1', yaml)
    yield qlw


class TestQueryList:
    def test_import(self):
        assert 'SectionqueryWidget' == SectionqueryWidget.__name__

    def test_construction(self, dummy_sectionquery):
        assert 'w23' == dummy_sectionquery.props.name

    def test_make_context(self, dummy_sectionquery, article_resources, sphinx_app):
        sphinx_app.env.resources = article_resources
        context = dict()
        result = dummy_sectionquery.make_context(context, sphinx_app)
        assert None is result
        assert 4 == context['result_count']
        results = context['results']
        assert 'f1/index' == results[0].docname
5