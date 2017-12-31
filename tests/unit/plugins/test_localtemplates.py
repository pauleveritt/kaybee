from kaybee.plugins.localtemplates.handlers import (
    handle_beforereaddocs,
)


class TestPluginLocalTemplates:
    def test_import(self):
        assert 'handle_beforereaddocs' == handle_beforereaddocs.__name__

    def test_handle_beforereaddocs(self, kb_app, sphinx_app, sphinx_env):
        sphinx_app.confdir = 'xyz'
        handle_beforereaddocs(kb_app, sphinx_app, sphinx_env, [])
        loaders = sphinx_app.builder.templates.loaders
        search_path = loaders[0].searchpath[0]
        assert sphinx_app.confdir in search_path
