import dectate
import pytest

from kaybee.plugins.resources.directive import ResourceDirective
from kaybee.plugins.resources.handlers import (
    handle_builderinited,
    initialize_resources_container,
    register_template_directory,
    add_directives,
    resource_into_html_context,
    dump_settings,
)


@pytest.fixture()
def valid_registration(kb_app):
    @kb_app.resource('article')
    def article1(*args):
        return

    dectate.commit(kb_app)
    yield article1


class TestResourcesBuilderInit:
    def test_import(self):
        assert 'handle_builderinited' == handle_builderinited.__name__

    def test_result(self, kb_app, sphinx_app):
        result = handle_builderinited(kb_app, sphinx_app)
        assert None is result


class TestResourcesDumpSettings:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_result(self, kb_app, sphinx_env):
        kb_app.config.resources = dict()
        sphinx_env.app.resources = dict()
        result = dump_settings(kb_app, sphinx_env)
        assert 'resources' in result


class TestResourcesTemplateDir:
    def test_import(self):
        assert 'register_template_directory' == \
               register_template_directory.__name__

    def test_result(self, kb_app, sphinx_app, sphinx_env, valid_registration):
        register_template_directory(kb_app, sphinx_app, sphinx_env,
                                    [])
        loaders = sphinx_app.builder.templates.loaders
        search_path = loaders[0].searchpath[0]
        assert 'tests/unit/plugins/resources' in search_path


class TestResourcesAddDirectives:
    def test_import(self):
        assert 'add_directives' == add_directives.__name__

    def test_result(self, mocker, kb_app, sphinx_app, sphinx_env,
                    valid_registration):
        mocker.patch.object(sphinx_app, 'add_directive')
        add_directives(kb_app, sphinx_app, sphinx_env,
                       [])
        sphinx_app.add_directive.assert_called_once_with('article',
                                                         ResourceDirective)


class TestResourcesResourceIntoHtml:
    def test_import(self):
        assert 'resource_into_html_context' == \
               resource_into_html_context.__name__

    def test_result(self, mocker, kb_app, sphinx_app, sphinx_env,
                    sample_resources):
        r3 = sample_resources['r1/r2/r3/index']
        sphinx_app.resources = {r3.docname: r3}
        pagename = r3.docname
        templatename = ''
        context = dict()
        doctree = dict()
        result = resource_into_html_context(kb_app, sphinx_app,
                                   pagename, templatename, context, doctree
                                   )
        assert 'resource' in context
        assert 'page.html' == result['templatename']


class TestResourcesInitializeContainer:
    def test_import(self):
        assert 'initialize_resources_container' == \
               initialize_resources_container.__name__

    def test_result(self, kb_app, sphinx_app, sphinx_env, valid_registration):
        initialize_resources_container(kb_app, sphinx_app, sphinx_env,
                                       [])
        assert hasattr(sphinx_app, 'resources')
