from kaybee.plugins.articles.handlers import (
    dump_settings,
)


class TestToctreeDumpSettings:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_result(self, kb_app, sphinx_env):
        kb_app.config.toctrees = dict()
        sphinx_env.app.toctrees = dict()
        result = dump_settings(kb_app, sphinx_env)
        assert 'toctrees' in result
