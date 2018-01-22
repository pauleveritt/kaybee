import dectate
import pytest

from kaybee.plugins.layouts.handlers import (
    initialize_layout,
    register_template_directory,
    layout_into_html_context,
    dump_settings,
)
from kaybee.plugins.layouts.base_layout import BaseLayout


# When I tried to put this into conftest.py, pytest inexplicably told
# inspect.getfile that we were in genericpage.conftest.py

@pytest.fixture()
def valid_layouts2(layouts_kb_app):
    @layouts_kb_app.layout('mylayout1')
    class Layout1(BaseLayout):
        pass

    @layouts_kb_app.layout('mylayout2')
    class Layout2(BaseLayout):
        pass

    dectate.commit(layouts_kb_app)
    yield (Layout1, Layout2)


class TestResourcesInitializeContainer:
    def test_import(self):
        assert 'initialize_layout' == \
               initialize_layout.__name__

    def test_theme_is_not_layout(self,
                                 layouts_kb_app,
                                 sphinx_app,
                                 sphinx_env,
                                 valid_layouts):
        initialize_layout(layouts_kb_app, sphinx_app, sphinx_env,
                          [])
        assert not hasattr(sphinx_app, 'layout')

    def test_theme_is_layout(self,
                             layouts_kb_app,
                             sphinx_app,
                             sphinx_env,
                             valid_layouts,
                             my_layout):
        sphinx_app.config.html_theme = my_layout
        initialize_layout(layouts_kb_app, sphinx_app, sphinx_env,
                          [])
        assert 'MyLayout' == sphinx_app.layout.__class__.__name__


class TestResourcesTemplateDir:
    def test_import(self):
        assert 'register_template_directory' == \
               register_template_directory.__name__

    def test_result(self, layouts_kb_app, sphinx_app, sphinx_env,
                    valid_layouts2, my_layout):
        sphinx_app.config.html_theme = my_layout
        register_template_directory(layouts_kb_app, sphinx_app,
                                    sphinx_env,
                                    [])
        loaders = sphinx_app.builder.templates.loaders
        search_path = loaders[0].searchpath[0]
        assert 'tests/unit/plugins/layouts' in search_path


class TestResourcesResourceIntoHtml:
    def test_import(self):
        assert 'layout_into_html_context' == \
               layout_into_html_context.__name__

    def test_with_layout(self, mocker, layouts_kb_app, sphinx_app,
                         sphinx_env):
        sphinx_app.layout = 88
        context = dict()
        doctree = ''
        layout_into_html_context(layouts_kb_app, sphinx_app,
                                 '', '', context,
                                 doctree
                                 )
        assert 88 == context['layout']

    def test_with_no_layout(self, mocker, layouts_kb_app, sphinx_app,
                            sphinx_env):
        context = dict()
        doctree = ''
        layout_into_html_context(layouts_kb_app, sphinx_app,
                                 '', '', context,
                                 doctree
                                 )
        assert 'layout' not in context


class TestResourcesDumpSettings:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_result(self, layouts_kb_app, sphinx_env):
        layouts_kb_app.config.layouts = dict()
        sphinx_env.app.layout = dict()
        result = dump_settings(layouts_kb_app, sphinx_env)
        assert 'layouts' in result
