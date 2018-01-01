import pytest

from kaybee.plugins.resources.base_resource import BaseResource
from kaybee.plugins.resources.directive import ResourceDirective


class ResourcesContainer:
    def __init__(self):
        self.resources = {}


@pytest.fixture
def sample_resources():
    root = BaseResource('index', 'resource', '')
    about = BaseResource('about', 'resource', '')
    r1 = BaseResource('r1/index', 'resource', '')
    r1about = BaseResource('r1/about', 'resource', '')
    r2 = BaseResource('r1/r2/index', 'resource', '')
    r2about = BaseResource('r1/r2/about', 'resource', '')
    r3 = BaseResource('r1/r2/r3/index', 'resource', '')
    r3about = BaseResource('r1/r2/r3/about', 'resource', '')
    r4 = BaseResource('r1/r2/r3/r4/index', 'resource', '')
    r4about = BaseResource('r1/r2/r3/r4/about', 'resource', '')

    resources = dict()
    for r in (root, about,
              r1, r1about,
              r2, r2about,
              r3, r3about,
              r4, r4about,
              ):
        resources[r.docname] = r

    yield resources


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
    # monkeypatch.setattr(ResourceDirective, 'get_resource_class',
    #                     lambda x: SampleResource)
    # monkeypatch.setattr(ResourceDirective, 'docname', 'somedocname')
    # monkeypatch.setattr(ResourceDirective, 'site', DummySite())
    bd = dummy_directive_class(
        dummy_directive_class.name, [], dict(), '', 0, 0, '', {}, {})
    bd.state = Dummy()
    bd.state.document = Dummy()
    bd.state.document.settings = Dummy()
    bd.state.document.settings.env = Dummy()
    bd.state.document.settings.env.docname = 'somedoc'
    bd.state.document.settings.env.resources = dict()

    yield bd
