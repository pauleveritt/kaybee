import dectate
import pytest

from kaybee.plugins.genericpage.action import GenericpageAction
from kaybee.plugins.genericpage.handlers import (
    initialize_genericpages_container,
    add_genericpage,
    genericpage_into_html_context,
    dump_settings,
)
from kaybee.plugins.genericpage.genericpage import Genericpage


@pytest.fixture()
def conflicting_gps(kb_app):
    @kb_app.genericpage()
    class Genericpage1(Genericpage):
        pass

    @kb_app.genericpage()
    class Genericpage2(Genericpage):
        pass

    yield (Genericpage1, Genericpage2)


@pytest.fixture()
def valid_gp(kb_app):
    @kb_app.genericpage()
    class Genericpage1(Genericpage):
        pass

    dectate.commit(kb_app)
    yield Genericpage1


@pytest.fixture()
def valid_gps(kb_app):
    @kb_app.genericpage()
    class Genericpage1(Genericpage):
        pass

    # This one should "override" the first one
    @kb_app.genericpage(order=10)
    class Genericpage2(Genericpage):
        pass

    dectate.commit(kb_app)
    yield (Genericpage1, Genericpage2)


@pytest.fixture()
def root_resource():
    class Props:
        pass

    class RootResource:
        def __init__(self):
            self.props = Props()

    yield RootResource()


class TestPluginGenericpage:
    def test_import(self):
        assert 'GenericpageAction' == GenericpageAction.__name__

    def test_construction(self, kb_app):
        dectate.commit(kb_app)
        assert True

    def test_identifier_default(self):
        da = GenericpageAction()
        assert '40' == da.identifier([])

    def test_identifiers_conflict(self, kb_app, conflicting_gps):
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(kb_app)

    def test_get_builtin_genericpage(self, kb_app):
        # No @kb.genericpage found in the docs project or any plugins it
        # installed, so get_genericpage should return the built-in class,
        # since none in registry.
        dectate.commit(kb_app)
        gp = GenericpageAction.get_genericpage(kb_app)
        assert 'Genericpage' == gp.__name__

    def test_get_single_genericpage(self, kb_app, valid_gp):
        # The docs project (or a third-party plugin) registers a single
        # "override"
        gp = GenericpageAction.get_genericpage(kb_app)
        assert valid_gp == gp

    def test_get_sorted_genericpage(self, kb_app, valid_gps):
        gp = GenericpageAction.get_genericpage(kb_app)
        assert valid_gps[1] == gp


class TestGeneripage:
    def test_import(self):
        assert 'Genericpage' == Genericpage.__name__

    def test_default_templatename(self, kb_app, valid_gp, root_resource):
        # Nothing on the root resource, so use default templatename 'page'

        resources = dict(index=root_resource)
        templatename = valid_gp.template(resources)
        assert 'page' == templatename

    def test_root_no_acquireds(self, kb_app, valid_gp, root_resource):
        # There's a root, but its props have no 'acquireds'
        resources = dict(index=root_resource)
        templatename = valid_gp.template(resources)
        assert 'page' == templatename

    def test_root_gp_templatename(self, kb_app, valid_gp, root_resource):
        # Root acquireds with 'genericpage' section
        root_resource.props.acquireds = dict(
            genericpage=dict(template='gp_custom')
        )
        resources = dict(index=root_resource)
        templatename = valid_gp.template(resources)
        assert 'gp_custom' == templatename

    def test_root_all_templatename(self, kb_app, valid_gp, root_resource):
        # Root acquireds with 'all' section
        root_resource.props.acquireds = dict(
            all=dict(template='all_custom')
        )
        resources = dict(index=root_resource)
        templatename = valid_gp.template(resources)
        assert 'all_custom' == templatename

    def test_repr(self):
        # The repr is primarily useful in pytest listing
        br = Genericpage('somepage')
        assert 'somepage' == repr(br)

    def test_to_json(self, root_resource):
        root_resource.props.acquireds = dict(
            genericpage=dict(template='gp_custom')
        )
        resources = dict(index=root_resource)

        about = Genericpage('about')
        actual = about.__json__(resources)
        assert 'about' == actual['docname']
        assert 'gp_custom' == actual['template']


class TestGenericpagesContainer:
    def test_import(self):
        assert 'initialize_genericpages_container' == \
               initialize_genericpages_container.__name__

    def test_result(self, kb_app, sphinx_app, sphinx_env):
        initialize_genericpages_container(kb_app, sphinx_app, sphinx_env,
                                          [])
        assert hasattr(sphinx_app, 'genericpages')


@pytest.fixture()
def foo_doctree():
    class Doctree:
        attributes = dict(source='foo.rst')

    yield Doctree()


class TestGenericpagesAdd:
    def test_import(self):
        assert 'add_genericpage' == \
               add_genericpage.__name__

    def test_noadd_genericpage(self, kb_app, sphinx_app, sphinx_env,
                               foo_doctree):
        # We have a resource for this docname, don't make add genericpage
        sphinx_app.resources = dict(
            foo=dict()
        )
        result = add_genericpage(kb_app, sphinx_app, foo_doctree)
        assert None is result

    def test_add_genericpage(self, kb_app, sphinx_app, sphinx_env,
                             foo_doctree,
                             valid_gp):
        sphinx_app.resources = dict(
            no_foo=dict()
        )
        sphinx_app.genericpages = dict()
        dectate.commit(kb_app)
        result = add_genericpage(kb_app, sphinx_app, foo_doctree)
        assert valid_gp == result.__class__
        assert 'foo' == result.docname
        assert 'foo' in sphinx_app.genericpages


class TestGenericpageIntoHtml:
    def test_import(self):
        assert 'genericpage_into_html_context' == \
               genericpage_into_html_context.__name__

    def test_result(self, mocker, kb_app, sphinx_app, sphinx_env,
                    sample_resources):
        index = sample_resources['index']
        sphinx_app.resources = {index.docname: index}
        about = Genericpage('r1/r2/about')
        sphinx_app.genericpages = {about.docname: about}
        pagename = about.docname
        templatename = ''
        context = dict()
        doctree = dict()
        result = genericpage_into_html_context(
            kb_app, sphinx_app, pagename, templatename, context, doctree
        )
        assert 'genericpage' in context
        assert 'page.html' == result['templatename']


class TestPluginGenerateDebugEvent:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_debug(self, kb_app, sphinx_env, valid_gps):
        sphinx_env.app.resources = dict(
            foo=dict()
        )
        sphinx_env.app.genericpages = dict(
            foo=Genericpage('foo')
        )
        genericpages = dump_settings(kb_app, sphinx_env)
        assert 'genericpages' in genericpages
        config = genericpages['genericpages']['config']
        assert 10 in config
        values = genericpages['genericpages']['values']
        assert 1 == len(values)
        assert 'foo' == values['foo']['docname']
