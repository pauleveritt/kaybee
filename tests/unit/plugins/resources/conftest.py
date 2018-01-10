import pytest

from kaybee.plugins.resources.directive import ResourceDirective


class DummySite:
    added_label = None

    def __init__(self):
        self.resources = dict()

    def add_reference(self, rtype, label, this_resource):
        self.added_label = label


class Dummy:
    pass


@pytest.fixture()
def dummy_props():
    class DummyProps:
        template = 'foo'
        label = 'somelabel'

    yield DummyProps


@pytest.fixture()
def dummy_resource_class(dummy_props):
    class DummyResource:

        def __init__(self, docname, rtype, content):
            self.docname = docname
            self.rtype = rtype
            self.content = content
            self.props = dummy_props()

    yield DummyResource


@pytest.fixture()
def dummy_directive_class():
    class DummyDirective(ResourceDirective):
        name = 'dummy_directive'

    yield DummyDirective


@pytest.fixture()
def dummy_directive(dummy_directive_class):
    bd = dummy_directive_class(
        dummy_directive_class.name, [], dict(), '', 0, 0, '', {}, {})
    bd.state = Dummy()
    bd.state.document = Dummy()
    bd.state.document.settings = Dummy()
    bd.state.document.settings.env = Dummy()
    bd.state.document.settings.env.docname = 'somedoc'
    bd.state.document.settings.env.app = Dummy()
    bd.state.document.settings.env.app.resources = dict()

    yield bd
