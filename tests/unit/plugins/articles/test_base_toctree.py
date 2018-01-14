import pytest

from kaybee.plugins.articles.base_toctree import BaseToctree


@pytest.fixture()
def dummy_entries():
    r = [
        ('x', 'f1/about')
    ]

    yield r


@pytest.fixture()
def dummy_toctree():
    yield BaseToctree()


@pytest.fixture()
def dummy_titles():
    class Title:
        def __init__(self, first_child):
            self.children = [first_child]

    yield {
        'about': Title('About'),
        'f1/about': Title('F1 About')
    }


class TestBaseToctree:
    def test_import(self):
        assert 'BaseToctree' == BaseToctree.__name__

    def test_construction(self, dummy_toctree):
        assert [] == dummy_toctree.entries

    def test_set_empty_entries_empty(self, dummy_toctree, article_resources):
        titles = []
        dummy_toctree.set_entries([], titles, article_resources)
        assert [] == dummy_toctree.entries

    def test_set_missing_resource(self, dummy_toctree,
                                  dummy_entries, dummy_titles):
        dummy_toctree.set_entries(dummy_entries, dummy_titles, dict())
        first = dummy_toctree.entries[0]
        assert 'f1/about' == first['href']
        assert 'F1 About' == first['title']
        assert None is first['resource']

    def test_set_entries_with_resource(self, dummy_toctree,
                                       dummy_entries, dummy_titles,
                                       article_resources):
        dummy_toctree.set_entries(dummy_entries, dummy_titles,
                                  article_resources)
        first = dummy_toctree.entries[0]
        assert 'f1/about' == first['href']
        assert 'F1 About' == first['title']
        assert 'f1/about' == first['resource'].docname
        assert 'article' is first['resource'].rtype

    def test_render(self, mocker,
                    dummy_toctree, html_builder, sphinx_app):
        mocker.patch.object(html_builder.templates, 'render')
        context = dict()
        dummy_toctree.render(html_builder, context, sphinx_app)
        html_builder.templates.render.assert_called_once_with(
            'toctree', context
        )
        assert sphinx_app == context['sphinx_app']
        assert dummy_toctree == context['toctree']
