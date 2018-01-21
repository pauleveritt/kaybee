from kaybee.plugins.settings.handlers import dump_settings


class TestPluginSettings:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_dump_settings(self, settings_kb_app, sphinx_env):
        settings = sphinx_env.config.kaybee_settings
        result = dump_settings(settings_kb_app, sphinx_env)
        assert settings == result['settings']
