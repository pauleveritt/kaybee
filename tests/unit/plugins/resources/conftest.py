import dectate
import pytest

from kaybee.plugins.resources.action import ResourceAction
from kaybee.plugins.resources.directive import ResourceDirective
from kaybee.utils.rst import (
    rst_document,
)
from kaybee.plugins.articles.article import Article


class Dummy:
    pass


@pytest.fixture()
def resources_kb_app():
    class app(dectate.App):
        resource = dectate.directive(ResourceAction)

    yield app


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
def dummy_article(dummy_resource_class):
    yield dummy_resource_class('article1', 'article', '')


@pytest.fixture()
def dummy_image_article():
    yaml = """
images:
    - usage: feature
      filename: img1.png    
    """
    yield Article('image_article1', 'article', yaml)


@pytest.fixture()
def dummy_directive_class():
    class DummyDirective(ResourceDirective):
        name = 'dummy_directive'

    yield DummyDirective


@pytest.fixture()
def dummy_references():
    class References(dict):
        def add_reference(self, *args):
            pass

    yield References()


@pytest.fixture()
def dummy_directive(dummy_directive_class, dummy_references):
    bd = dummy_directive_class(
        dummy_directive_class.name, [], dict(), '', 0, 0, '', {}, {})
    bd.state = Dummy()
    bd.state.document = Dummy()
    bd.state.document.settings = Dummy()
    bd.state.document.settings.env = Dummy()
    bd.state.document.settings.env.docname = 'somedoc'
    bd.state.document.settings.env.resources = dict()
    bd.state.document.settings.env.references = dummy_references

    yield bd


@pytest.fixture()
def dummy_reference():
    class DummyReference:
        def __init__(self):
            self.props = Dummy()
            self.props.label = 'reference1'

    yield DummyReference()


@pytest.fixture()
def dummy_doctree():
    source = """\
=============
Test *Simple*
=============

Body.
        """
    yield rst_document(source)
