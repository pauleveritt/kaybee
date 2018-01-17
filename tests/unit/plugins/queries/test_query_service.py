import pytest

from kaybee.plugins.queries.service import Query
from tests.unit.plugins.queries.conftest import (
    Article,
    Section,
)


class TestQueryService:
    def test_import(self):
        assert 'Query' == Query.__name__

    def test_construction(self):
        q = Query('doc1')
        assert 'doc1' == q.docname

    @pytest.mark.parametrize('filter_key, filter_value, expected', [
        (None, 'article', 'About'),
        ('rtype', 'article', 'About'),
        ('sort_value', 'title', 'About'),
        ('reverse', True, 'Z Last weights first'),
    ])
    def test_filter_resources(self, query_resources, filter_key, filter_value,
                              expected):
        # No filter applied
        if filter_key is None:
            kw = {}
        else:
            kw = {filter_key: filter_value}
        results = Query.filter_collection(query_resources, **kw)
        assert expected == results[0].title

    def test_filter_resources_parent(self, query_resources):
        published = 'published: 2015-01-01 01:23'
        parent = Section('section2/index', 'section', published)
        parent.title = 'Parent'
        child = Article('section2/article2', 'article', published)
        child.title = 'Child'
        query_resources[parent.docname] = parent
        query_resources[child.docname] = child
        kw = dict(parent_name='section2/index')
        results = Query.filter_collection(query_resources, **kw)
        assert len(results) == 1
        assert 'Child' == results[0].title

    def test_filter_resources_props(self, query_resources):
        props = [
            dict(key='template', value='I am c1'),
        ]
        kw = dict(props=props)
        results = Query.filter_collection(query_resources, **kw)
        assert 1 == len(results)
        assert 'About' == results[0].title

    def test_filter_resources_empty_props(self, query_resources):
        props = [
            dict(key='template', value=None),
        ]
        kw = dict(props=props)
        results = Query.filter_collection(query_resources, **kw)
        assert 6 == len(results)
        assert 'About' == results[0].title

    def test_filter_resources_limit(self, query_resources):
        # No filter applied
        results = Query.filter_collection(query_resources, limit=2)
        assert len(results) == 2

    @pytest.mark.parametrize('field, reverse, expected_title', [
        ('title', False, 'About'),
        ('title', True, 'Z Last weights first'),
    ])
    def test_filter_resources_sort(self, query_resources, field, reverse,
                                   expected_title):
        results = Query.filter_collection(query_resources, sort_value=field,
                                          reverse=reverse)
        first_title = results[0].title
        assert expected_title == first_title

    def test_filter_resources_sort_value_none(self, query_resources):
        results = Query.filter_collection(query_resources, sort_value=None)
        first_title = results[0].title
        assert 'Second should sort ahead of first' == first_title

    def test_filter_resources_sort_value_not_title(self, query_resources):
        results = Query.filter_collection(query_resources,
                                          sort_value='template',
                                          reverse=True)
        # Remember, we reversed based on template
        last_template = results[0].props.template
        assert 'I am c2' == last_template

    def test_filter_resources_sort_title_reverse(self, query_resources):
        results = Query.filter_collection(query_resources,
                                          sort_value='title',
                                          reverse=True)
        first_title = results[0].title
        assert 'Z Last weights first' == first_title

