import dectate

from kaybee.plugins.genericpage.genericpage import Genericpage
from kaybee.plugins.genericpage.handlers import (
    initialize_genericpages_container,
    add_genericpage,
    genericpage_into_html_context,
    dump_settings,
)


class TestGenericpagesContainer:
    def test_import(self):
        assert 'initialize_genericpages_container' == \
               initialize_genericpages_container.__name__

    def test_result(self, genericpages_kb_app, sphinx_app, sphinx_env):
        initialize_genericpages_container(genericpages_kb_app, sphinx_app,
                                          sphinx_env,
                                          [])
        assert hasattr(sphinx_app, 'genericpages')


class TestGenericpagesAdd:
    def test_import(self):
        assert 'add_genericpage' == \
               add_genericpage.__name__

    def test_noadd_genericpage(self, genericpages_kb_app, sphinx_app,
                               foo_doctree):
        # We have a resource for this docname, don't make add genericpage
        sphinx_app.resources = dict(
            foo=dict()
        )
        result = add_genericpage(genericpages_kb_app, sphinx_app, foo_doctree)
        assert None is result

    def test_add_genericpage(self, genericpages_kb_app, sphinx_app,
                             foo_doctree,
                             valid_gp):
        sphinx_app.resources = dict(
            no_foo=dict()
        )
        sphinx_app.genericpages = dict()
        dectate.commit(genericpages_kb_app)
        result = add_genericpage(genericpages_kb_app, sphinx_app, foo_doctree)
        assert valid_gp == result.__class__
        assert 'foo' == result.docname
        assert 'foo' in sphinx_app.genericpages


class TestGenericpageIntoHtml:
    def test_import(self):
        assert 'genericpage_into_html_context' == \
               genericpage_into_html_context.__name__

    def test_has_resource(self, genericpages_kb_app, sphinx_app,
                          sample_resources):
        index = sample_resources['index']
        sphinx_app.resources = {index.docname: index}
        pagename = index.docname
        templatename = ''
        context = dict()
        doctree = dict()
        result = genericpage_into_html_context(
            genericpages_kb_app, sphinx_app, pagename, templatename, context,
            doctree
        )
        assert {} == context

    def test_has_gp(self, genericpages_kb_app, sphinx_app, sample_resources):
        index = sample_resources['index']
        sphinx_app.resources = {index.docname: index}
        about = Genericpage('r1/r2/about')
        sphinx_app.genericpages = {about.docname: about}
        pagename = about.docname
        templatename = ''
        context = dict()
        doctree = dict()
        result = genericpage_into_html_context(
            genericpages_kb_app, sphinx_app, pagename, templatename, context,
            doctree
        )
        assert 'genericpage' in context
        assert 'page.html' == result['templatename']

    def test_not_has_gp(self, genericpages_kb_app, sphinx_app,
                        sample_resources):
        index = sample_resources['index']
        sphinx_app.resources = {index.docname: index}
        about = Genericpage('r1/r2/about')
        sphinx_app.genericpages = {}
        pagename = about.docname
        templatename = ''
        context = dict()
        doctree = dict()
        result = genericpage_into_html_context(
            genericpages_kb_app, sphinx_app, pagename, templatename, context,
            doctree
        )
        assert 'genericpage' not in context
        assert None is result


class TestPluginGenerateDebugEvent:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_debug(self, genericpages_kb_app, sphinx_env, valid_gps):
        sphinx_env.app.resources = dict(
            foo=dict()
        )
        sphinx_env.app.genericpages = dict(
            foo=Genericpage('foo')
        )
        genericpages = dump_settings(genericpages_kb_app, sphinx_env)
        assert 'genericpages' in genericpages
        config = genericpages['genericpages']['config']
        assert 10 in config
        values = genericpages['genericpages']['values']
        assert 1 == len(values)
        assert 'foo' == values['foo']['docname']
