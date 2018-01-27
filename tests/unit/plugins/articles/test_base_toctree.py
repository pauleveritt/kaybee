import pytest
from datetime import datetime

from kaybee.plugins.articles.base_toctree import BaseToctree


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

    def test_set_entries_no_is_published(self, dummy_toctree,
                                         dummy_entries, dummy_titles,
                                         article_resources):
        f1about = article_resources['f1/about']
        f1about.props.published = datetime(2030, 1, 1)
        dummy_toctree.set_entries(dummy_entries, dummy_titles,
                                  article_resources)
        assert [] == dummy_toctree.entries

    @pytest.mark.parametrize('current_docname, target_docname, expected', [
        ('2018/index', '2018/about', 'about'),
        ('2018/about', '2018/contact', 'contact'),
        ('2018/01/01/about', '2018/01/01/contact', 'contact'),
        ('2018/01/01/about', '2001/12/12/about', '../../../2001/12/12/about'),
    ])
    def test_pathto(self, dummy_toctree,
                    current_docname, target_docname, expected):
        dummy_toctree.docname = current_docname
        assert expected == dummy_toctree.pathto_docname(target_docname)

    def test_render(self, mocker,
                    dummy_toctree, html_builder, sphinx_app):
        # Turn on toctree support
        sphinx_app.config.kaybee_settings.articles.use_toctree = True
        mocker.patch.object(html_builder.templates, 'render')
        context = dict()
        dummy_toctree.render(html_builder, context, sphinx_app)
        html_builder.templates.render.assert_called_once_with(
            'toctree.html', context
        )
        assert sphinx_app == context['sphinx_app']
        assert dummy_toctree == context['toctree']
