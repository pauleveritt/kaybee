import pytest
from kaybee.plugins.articles.querylist import QuerylistWidget


@pytest.fixture()
def dummy_querylist():
    yaml = """
    name: w23
    queries:
        - label: Recent Blog Posts
          query:
              rtype: section
              limit: 5        
    """
    qlw = QuerylistWidget('widget1', 'widget1', yaml)
    yield qlw


class TestQueryList:
    def test_import(self):
        assert 'QuerylistWidget' == QuerylistWidget.__name__

    def test_construction(self, dummy_querylist):
        assert 'w23' == dummy_querylist.props.name

    def test_make_context(self, dummy_querylist, article_resources, sphinx_app):
        sphinx_app.resources = article_resources
        context = dict()
        result = dummy_querylist.make_context(context, sphinx_app)
        assert None is result
        first_result = context['result_sets'][0]
        assert 'Recent Blog Posts' == first_result['label']
        assert 'f1/index' == first_result['results'][0].docname
