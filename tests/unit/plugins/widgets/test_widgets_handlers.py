import dectate
import pytest
from docutils import nodes

from kaybee.plugins.widgets.directive import WidgetDirective
from kaybee.plugins.widgets.handlers import (
    add_widget_node,
    initialize_widgets_container,
    register_template_directory,
    register_widget_directive,
    render_widgets,
    dump_settings,
)
from kaybee.plugins.widgets.node import widget


@pytest.fixture()
def dummy_doctree():
    class Doctree:
        def traverse(self):
            pass

    yield Doctree()


@pytest.fixture()
def dummy_node():
    class Node:
        def __init__(self):
            self.name = 'listing'

        def replace_self(self):
            pass

    yield Node()


@pytest.fixture()
def dummy_widget():
    class DummyWidget:
        def render(self, *args):
            return 'some html string'

    yield DummyWidget()


@pytest.fixture()
def valid_registration(kb_app):
    @kb_app.widget('listing')
    def listing1(*args):
        return

    dectate.commit(kb_app)
    yield listing1


class TestAddNode:
    def test_import(self):
        assert 'add_widget_node' == add_widget_node.__name__

    def test_call(self, mocker, kb_app, widgets_sphinx_app):
        mocker.patch.object(widgets_sphinx_app, 'add_node')
        add_widget_node(kb_app, widgets_sphinx_app)
        widgets_sphinx_app.add_node.assert_called_once_with(
            widget
        )

class TestWidgetsInitializeContainer:
    def test_import(self):
        assert 'initialize_widgets_container' == \
               initialize_widgets_container.__name__

    def test_result(self, kb_app, sphinx_app, sphinx_env):
        initialize_widgets_container(kb_app, sphinx_app, sphinx_env,
                                     [])
        assert hasattr(sphinx_app, 'widgets')


class TestWidgetsRenderWidgets:
    def test_import(self):
        assert 'render_widgets' == render_widgets.__name__

    def test_render(self, mocker, kb_app, dummy_doctree, widgets_sphinx_app,
                    dummy_node, dummy_widget):
        widgets_sphinx_app.widgets['listing'] = dummy_widget
        mocker.patch.object(dummy_doctree, 'traverse',
                            return_value=[dummy_node])
        mocker.patch.object(nodes, 'raw', return_value=987)
        mocker.patch.object(dummy_node, 'replace_self')
        fromdocname = 'fromsomedoc'
        render_widgets(kb_app, widgets_sphinx_app, dummy_doctree,
                       fromdocname)
        dummy_doctree.traverse.assert_called_once_with(widget)
        nodes.raw.assert_called_once_with(
            '', 'some html string', format='html'
        )
        dummy_node.replace_self.assert_called_once_with([987])


class TestWidgetsTemplateDir:
    def test_import(self):
        assert 'register_template_directory' == \
               register_template_directory.__name__

    def test_result(self, kb_app, sphinx_app, sphinx_env, valid_registration):
        register_template_directory(kb_app, sphinx_app, sphinx_env,
                                    [])
        loaders = sphinx_app.builder.templates.loaders
        search_path = loaders[0].searchpath[0]
        assert 'tests/unit/plugins/widgets' in search_path


class TestRegisterDirective:
    def test_import(self):
        assert 'register_widget_directive' == \
               register_widget_directive.__name__

    def test_register(self, mocker, kb_app, widgets_sphinx_app, sphinx_env,
                      valid_registration):
        mocker.patch.object(widgets_sphinx_app, 'add_directive')
        register_widget_directive(kb_app, widgets_sphinx_app, sphinx_env, [])
        widgets_sphinx_app.add_directive.assert_called_once_with(
            'listing', WidgetDirective
        )


class TestWidgetsDumpSettings:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_result(self, kb_app, sphinx_env):
        kb_app.config.widgets = dict()
        sphinx_env.app.widgets = dict()
        result = dump_settings(kb_app, sphinx_env)
        assert 'widgets' in result
