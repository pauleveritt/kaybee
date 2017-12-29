import dectate
import pytest
from docutils.readers import doctree
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.plugins.events import EventAction


@pytest.fixture()
def kb_app():
    class app(dectate.App):
        event = dectate.directive(EventAction)

    yield app


@pytest.fixture()
def sphinx_app():
    class SphinxApp:
        def connect(self, event_name, callable):
            pass

    app: Sphinx = SphinxApp()
    yield app


@pytest.fixture()
def sphinx_env():
    env: BuildEnvironment = dict()
    yield env


@pytest.fixture()
def sphinx_doctree():
    dt: doctree = dict()
    yield dt


@pytest.fixture()
def html_builder():
    class Builder:
        pass
    builder: StandaloneHTMLBuilder = Builder()
    yield builder
