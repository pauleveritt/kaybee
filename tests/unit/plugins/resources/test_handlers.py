import dectate
import pytest

from kaybee.plugins.resources.handlers import (
    handle_builderinited,
    dump_settings,
    register_template_directory,
)


@pytest.fixture()
def valid_registration(kb_app):
    @kb_app.resource('article')
    def article1(*args):
        return

    dectate.commit(kb_app)
    yield article1


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


class TestPluginResourcesTemplateDirEvent:
    def test_import(self):
        assert 'register_template_directory' == \
               register_template_directory.__name__

    def test_result(self, mocker, kb_app, sphinx_app, sphinx_env,
                    valid_registration):
        register_template_directory(kb_app, sphinx_app, sphinx_env,
                                    [])
        loaders = sphinx_app.builder.templates.loaders
        search_path = loaders[0].searchpath[0]
        assert 'tests/unit/plugins/resources' in search_path
