import dectate
import pytest

from kaybee.plugins.articles.handlers import (
    render_toctrees,
    dump_settings,
)
from kaybee.plugins.articles.base_toctree import BaseToctree


@pytest.fixture()
def valid_registration(kb_app):
    @kb_app.toctree()
    class Toctree(BaseToctree):
        pass

    dectate.commit(kb_app)
    yield (Toctree,)


class TestRenderToctrees:
    def test_import(self):
        assert 'render_toctrees' == render_toctrees.__name__

    def test_not_hidden(self, kb_app, sphinx_app, valid_registration,
                        dummy_doctree, article_env, article_resources,
                        mocker,
                        ):
        sphinx_app.env = article_env
        sphinx_app.resources = article_resources
        node = dummy_doctree.traverse()[0]
        mocker.patch.object(node, 'replace_self')
        fromdocname = ''
        render_toctrees(kb_app, sphinx_app, dummy_doctree,
                        fromdocname)
        node.replace_self.assert_called()

    def test_hidden(self, kb_app, sphinx_app, valid_registration,
                    dummy_doctree, article_env, article_resources,
                    mocker,
                    ):
        sphinx_app.env = article_env
        sphinx_app.resources = article_resources
        node = dummy_doctree.traverse()[0]
        node.attributes['hidden'] = True
        mocker.patch.object(node, 'replace_self')
        fromdocname = ''
        render_toctrees(kb_app, sphinx_app, dummy_doctree,
                        fromdocname)
        node.replace_self.assert_not_called()

    def test_no_nodes(self, kb_app, sphinx_app, valid_registration,
                      dummy_doctree, article_env, article_resources,
                      mocker,
                      ):
        sphinx_app.env = article_env
        sphinx_app.resources = article_resources
        dummy_doctree.dummy_nodes = []
        mocker.patch.object(valid_registration[0], 'set_entries')
        fromdocname = ''
        render_toctrees(kb_app, sphinx_app, dummy_doctree,
                        fromdocname)
        valid_registration[0].set_entries.assert_not_called()


class TestToctreeDumpSettings:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_result(self, kb_app, sphinx_env):
        kb_app.config.toctrees = dict()
        sphinx_env.app.toctrees = dict()
        result = dump_settings(kb_app, sphinx_env)
        assert 'toctrees' in result
