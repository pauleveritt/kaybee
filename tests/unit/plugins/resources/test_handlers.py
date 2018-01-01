from kaybee.plugins.resources.handlers import (
    handle_builderinited,
    dump_settings
)


class TestPluginResourcesBuilderInitEvent:
    def test_import(self):
        assert 'handle_builderinited' == handle_builderinited.__name__

    def test_result(self, kb_app, sphinx_app):
        result = handle_builderinited(kb_app, sphinx_app)
        assert None is result


class TestPluginResourcesDumpSettingsEvent:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_result(self, kb_app, sphinx_env):
        result = dump_settings(kb_app, sphinx_env)
        assert 'resources' in result
