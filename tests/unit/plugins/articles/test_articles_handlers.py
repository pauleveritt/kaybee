import dectate
import pytest

from kaybee.plugins.articles.handlers import (
    articles_into_html_context,
    register_template_directory,
    render_toctrees,
    resource_toctrees,
    stamp_excerpt,
    dump_settings,
)
from kaybee.plugins.articles.base_toctree import BaseToctree


@pytest.fixture()
def valid_registration(articles_kb_app):
    @articles_kb_app.toctree()
    class Toctree(BaseToctree):
        pass

    dectate.commit(articles_kb_app)
    yield (Toctree,)


class TestArticlesTemplateDir:
    def test_import(self):
        assert 'register_template_directory' == \
               register_template_directory.__name__

    def test_result(self, articles_kb_app, sphinx_app, sphinx_env,
                    valid_registration):
        register_template_directory(articles_kb_app, sphinx_app, sphinx_env,
                                    [])
        loaders = sphinx_app.builder.templates.loaders
        search_path = loaders[0].searchpath[0]
        assert 'tests/unit/plugins/articles' in search_path


class TestStampExcerpt:
    def test_import(self):
        assert 'stamp_excerpt' == stamp_excerpt.__name__

    def test_run_without_resource(self, kb_app, sphinx_app,
                                  dummy_article, excerpt):
        sphinx_app.confdir = '/tmp'
        excerpt.attributes = dict(source='/tmp/article1.rst')
        sphinx_app.resources = dict()
        assert None is getattr(dummy_article, 'excerpt', None)
        stamp_excerpt(kb_app, sphinx_app, excerpt)
        assert None is getattr(dummy_article, 'excerpt')

    def test_run_auto_excerpt(self, kb_app, sphinx_app,
                              dummy_article, excerpt):
        sphinx_app.confdir = '/tmp'
        excerpt.attributes = dict(source='/tmp/article1.rst')
        sphinx_app.resources = dict(
            article1=dummy_article
        )
        assert None is getattr(dummy_article, 'excerpt', None)
        stamp_excerpt(kb_app, sphinx_app, excerpt)
        assert 'First paragraph.' == dummy_article.excerpt

    def test_run_no_auto_excerpt(self, kb_app, sphinx_app,
                                 dummy_article, excerpt):
        sphinx_app.confdir = '/tmp'
        excerpt.attributes = dict(source='/tmp/article1.rst')
        dummy_article.props.excerpt = None
        dummy_article.props.auto_excerpt = 0
        sphinx_app.resources = dict(
            article1=dummy_article
        )
        assert None is getattr(dummy_article, 'excerpt', None)
        stamp_excerpt(kb_app, sphinx_app, excerpt)
        assert None is dummy_article.excerpt

    def test_run_manual_excerpt(self, kb_app, sphinx_app,
                                dummy_article, excerpt):
        sphinx_app.confdir = '/tmp'
        excerpt.attributes = dict(source='/tmp/article1.rst')
        dummy_article.props.excerpt = 'Manual Excerpt.'
        sphinx_app.resources = dict(
            article1=dummy_article
        )
        assert None is getattr(dummy_article, 'excerpt', None)
        stamp_excerpt(kb_app, sphinx_app, excerpt)
        assert 'Manual Excerpt.' == dummy_article.excerpt

    def test_run_two_paragraphs(self, kb_app, sphinx_app,
                                dummy_article, excerpt):
        sphinx_app.confdir = '/tmp'
        excerpt.attributes = dict(source='/tmp/article1.rst')
        dummy_article.props.auto_excerpt = 2
        sphinx_app.resources = dict(
            article1=dummy_article
        )
        assert None is getattr(dummy_article, 'excerpt', None)
        stamp_excerpt(kb_app, sphinx_app, excerpt)
        assert 'First paragraph. Second paragraph.' == dummy_article.excerpt


class TestArticlesIntoHtml:
    def test_import(self):
        assert 'articles_into_html_context' == \
               articles_into_html_context.__name__

    def test_navmenu(self, articles_kb_app, sphinx_app,
                     article_resources):
        f1 = article_resources['f1/index']
        f1.props.in_nav = True
        sphinx_app.resources = article_resources
        context = dict()
        articles_into_html_context(articles_kb_app, sphinx_app,
                                   '', '', context, dict()
                                   )
        assert 'navmenu' in context
        assert f1 in context['navmenu']


class TestRenderToctrees:
    def test_import(self):
        assert 'render_toctrees' == render_toctrees.__name__

    def test_not_use_toctree(self, articles_kb_app, sphinx_app,
                             valid_registration,
                             dummy_doctree, article_env, article_resources,
                             mocker,
                             ):
        # By default toctree support is turned off
        sphinx_app.env = article_env
        sphinx_app.resources = article_resources
        node = dummy_doctree.traverse()[0]
        mocker.patch.object(node, 'replace_self')
        fromdocname = ''
        render_toctrees(articles_kb_app, sphinx_app, dummy_doctree,
                        fromdocname)
        node.replace_self.assert_not_called()

    def test_not_hidden(self, articles_kb_app, sphinx_app, valid_registration,
                        dummy_doctree, article_env, article_resources,
                        mocker,
                        ):
        # Turn on toctree support
        sphinx_app.config.kaybee_settings.articles.use_toctree = True
        sphinx_app.env = article_env
        sphinx_app.resources = article_resources
        node = dummy_doctree.traverse()[0]
        mocker.patch.object(node, 'replace_self')
        fromdocname = 'some/path/index'
        render_toctrees(articles_kb_app, sphinx_app, dummy_doctree,
                        fromdocname)
        node.replace_self.assert_called()

    def test_hidden(self, articles_kb_app, sphinx_app, valid_registration,
                    dummy_doctree, article_env, article_resources,
                    mocker,
                    ):
        # Turn on toctree support
        sphinx_app.config.kaybee_settings.articles.use_toctree = True
        sphinx_app.env = article_env
        sphinx_app.resources = article_resources
        node = dummy_doctree.traverse()[0]
        node.attributes['hidden'] = True
        mocker.patch.object(node, 'replace_self')
        fromdocname = 'some/path/index'
        render_toctrees(articles_kb_app, sphinx_app, dummy_doctree,
                        fromdocname)
        node.replace_self.assert_not_called()

    def test_no_nodes(self, articles_kb_app, sphinx_app, valid_registration,
                      dummy_doctree, article_env, article_resources,
                      mocker,
                      ):
        # Turn on toctree support
        sphinx_app.config.kaybee_settings.articles.use_toctree = True
        sphinx_app.env = article_env
        sphinx_app.resources = article_resources
        dummy_doctree.dummy_nodes = []
        mocker.patch.object(valid_registration[0], 'set_entries')
        fromdocname = ''
        render_toctrees(articles_kb_app, sphinx_app, dummy_doctree,
                        fromdocname)
        valid_registration[0].set_entries.assert_not_called()


class TestResourceToctrees:
    def test_import(self):
        assert 'resource_toctrees' == resource_toctrees.__name__

    def test_run_with_resource(self, articles_kb_app, sphinx_app,
                               dummy_doctree,
                               dummy_article):
        sphinx_app.confdir = '/tmp'
        dummy_doctree.attributes = dict(source='/tmp/article1.rst')
        sphinx_app.resources = dict(
            article1=dummy_article
        )
        assert [] == dummy_article.toctree
        resource_toctrees(articles_kb_app, sphinx_app, dummy_doctree)
        assert ['f1/about'] == dummy_article.toctree

    def test_run_without_resource(self, articles_kb_app, sphinx_app,
                                  dummy_doctree,
                                  dummy_article):
        sphinx_app.confdir = '/tmp'
        dummy_doctree.attributes = dict(source='/tmp/article1.rst')
        sphinx_app.resources = dict()
        assert [] == dummy_article.toctree
        resource_toctrees(articles_kb_app, sphinx_app, dummy_doctree)
        assert [] == dummy_article.toctree


class TestToctreeDumpSettings:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_result(self, articles_kb_app, sphinx_env):
        # Turn on toctree support
        sphinx_env.app.config.kaybee_settings.articles.use_toctree = True
        articles_kb_app.config.toctrees = dict()
        sphinx_env.app.toctrees = dict()
        result = dump_settings(articles_kb_app, sphinx_env)
        assert 'toctrees' in result
