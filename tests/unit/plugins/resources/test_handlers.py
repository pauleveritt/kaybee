import shutil
from inspect import getfile
from pathlib import Path

import dectate
import pytest

from kaybee.plugins.resources.directive import ResourceDirective
from kaybee.plugins.resources.handlers import (
    handle_builderinited,
    initialize_resources_container,
    register_template_directory,
    add_directives,
    stamp_title,
    resource_into_html_context,
    dump_settings,
)
from plugins.resources.handlers import process_field_handlers


@pytest.fixture()
def get_module_dir():
    # Need to get path to image in this tests's directory
    gf = getfile(get_module_dir)
    yield Path(gf).parent


@pytest.fixture()
def valid_registration(resources_kb_app):
    @resources_kb_app.resource('article')
    def article1(*args):
        return

    dectate.commit(resources_kb_app)
    yield article1


class TestResourcesBuilderInit:
    def test_import(self):
        assert 'handle_builderinited' == handle_builderinited.__name__

    def test_result(self, resources_kb_app, sphinx_app):
        result = handle_builderinited(resources_kb_app, sphinx_app)
        assert None is result


class TestResourcesDumpSettings:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_result(self, resources_kb_app, sphinx_env):
        resources_kb_app.config.resources = dict()
        sphinx_env.resources = dict()
        result = dump_settings(resources_kb_app, sphinx_env)
        assert 'resources' in result


class TestResourcesTemplateDir:
    def test_import(self):
        assert 'register_template_directory' == \
               register_template_directory.__name__

    def test_result(self, resources_kb_app, sphinx_app, sphinx_env,
                    valid_registration):
        register_template_directory(resources_kb_app, sphinx_app, sphinx_env,
                                    [])
        loaders = sphinx_app.builder.templates.loaders
        search_path = loaders[0].searchpath[0]
        assert 'tests/unit/plugins/resources' in search_path


class TestResourcesAddDirectives:
    def test_import(self):
        assert 'add_directives' == add_directives.__name__

    def test_result(self, mocker, resources_kb_app, sphinx_app, sphinx_env,
                    valid_registration):
        mocker.patch.object(sphinx_app, 'add_directive')
        add_directives(resources_kb_app, sphinx_app, sphinx_env,
                       [])
        sphinx_app.add_directive.assert_called_once_with('article',
                                                         ResourceDirective)


class TestProcessFieldHandlers:
    def test_import(self):
        assert 'process_field_handlers' == process_field_handlers.__name__

    def test_article_has_image(self, dummy_image_article):
        assert 'feature' == dummy_image_article.props.images[0].usage

    def test_run_with_resource(self,
                               mocker,
                               resources_kb_app,
                               sphinx_app,
                               dummy_image_article,
                               get_module_dir):
        mocker.patch('shutil.copy')
        sphinx_app.env.srcdir = get_module_dir
        sphinx_app.outdir = '/tmp'
        sphinx_app.env.resources = dict(
            image_article_1=dummy_image_article
        )
        process_field_handlers(resources_kb_app, sphinx_app,
                               sphinx_app.env)
        assert 1 == shutil.copy.call_count

    def test_run_without_resource(self,
                                  mocker,
                                  resources_kb_app,
                                  sphinx_app,
                                  dummy_image_article,
                                  get_module_dir):
        mocker.patch('shutil.copy')
        sphinx_app.env.srcdir = get_module_dir
        sphinx_app.outdir = '/tmp'
        sphinx_app.env.resources = dict()
        process_field_handlers(resources_kb_app, sphinx_app,
                               sphinx_app.env)
        assert 0 == shutil.copy.call_count


class TestStampTitle:
    def test_import(self):
        assert 'stamp_title' == stamp_title.__name__

    def test_run_with_resource(self, resources_kb_app, sphinx_app,
                               dummy_doctree,
                               dummy_article):
        sphinx_app.confdir = '/tmp'
        dummy_doctree.attributes = dict(source='/tmp/article1.rst')
        sphinx_app.env.resources = dict(
            article1=dummy_article
        )
        assert None is getattr(dummy_article, 'title', None)
        stamp_title(resources_kb_app, sphinx_app, dummy_doctree)
        assert 'Test Simple' == dummy_article.title

    def test_run_without_resource(self, resources_kb_app, sphinx_app,
                                  dummy_doctree,
                                  dummy_article):
        sphinx_app.confdir = '/tmp'
        dummy_doctree.attributes = dict(source='/tmp/article1.rst')
        sphinx_app.env.resources = dict()
        assert None is getattr(dummy_article, 'title', None)
        stamp_title(resources_kb_app, sphinx_app, dummy_doctree)
        assert False is getattr(dummy_article, 'title', False)


class TestResourcesResourceIntoHtml:
    def test_import(self):
        assert 'resource_into_html_context' == \
               resource_into_html_context.__name__

    def test_with_resource(self, resources_kb_app, sphinx_app,
                           sample_resources):
        r3 = sample_resources['r1/r2/r3/index']
        sphinx_app.env.resources = {r3.docname: r3}
        pagename = r3.docname
        templatename = ''
        context = dict()
        doctree = dict()
        result = resource_into_html_context(resources_kb_app, sphinx_app,
                                            pagename, templatename, context,
                                            doctree
                                            )
        assert 'resource' in context
        assert 'resources' in context
        assert 'page.html' == result['templatename']

    def test_no_resource(self, resources_kb_app, sphinx_app,
                         sample_resources):
        r3 = sample_resources['r1/r2/r3/index']
        sphinx_app.env.resources = {}
        pagename = r3.docname
        templatename = ''
        context = dict()
        doctree = dict()
        result = resource_into_html_context(resources_kb_app, sphinx_app,
                                            pagename, templatename, context,
                                            doctree
                                            )
        assert 'resource' not in context
        assert None is result


class TestResourcesInitializeContainer:
    def test_import(self):
        assert 'initialize_resources_container' == \
               initialize_resources_container.__name__

    def test_initialize(self, resources_kb_app, sphinx_app, sphinx_env):
        assert not hasattr(sphinx_app.env, 'resources')
        initialize_resources_container(resources_kb_app, sphinx_app,
                                       sphinx_env,
                                       [])
        assert hasattr(sphinx_app.env, 'resources')
