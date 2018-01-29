import dectate
import pytest

from kaybee.plugins.widgets.directive import WidgetDirective
from kaybee.plugins.widgets.action import WidgetAction


class Dummy:
    pass


@pytest.fixture()
def widgets_kb_app():
    class widgets_kb_app(dectate.App):
        widget = dectate.directive(WidgetAction)

    yield widgets_kb_app


@pytest.fixture()
def dummy_props():
    class DummyProps:
        template = 'foo'
        label = 'somelabel'

    yield DummyProps


@pytest.fixture()
def dummy_widget_class(dummy_props):
    class DummyWidget:

        def __init__(self, docname, wtype, content):
            self.docname = docname
            self.wtype = wtype
            self.content = content
            self.props = dummy_props()

    yield DummyWidget


@pytest.fixture()
def dummy_directive_class():
    class DummyDirective(WidgetDirective):
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
    bd.state.document.settings.env.app.widgets = dict()

    yield bd


@pytest.fixture()
def widgets_sphinx_app(sphinx_app):
    sphinx_app.widgets = dict()
    sphinx_app.resources = dict()
    sphinx_app.references = dict()

    yield sphinx_app
