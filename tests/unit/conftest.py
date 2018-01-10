import dectate
import pytest
from docutils.readers import doctree
from pydantic import BaseModel
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.plugins.debugdumper.action import DumperAction
from kaybee.plugins.debugdumper.settings import DebugdumperModel
from kaybee.plugins.events import EventAction
from kaybee.plugins.genericpage.action import GenericpageAction
from kaybee.plugins.resources.action import ResourceAction
from kaybee.plugins.widgets.action import WidgetAction


@pytest.fixture()
def kb_app():
    class app(dectate.App):
        dumper = dectate.directive(DumperAction)
        event = dectate.directive(EventAction)
        resource = dectate.directive(ResourceAction)
        genericpage = dectate.directive(GenericpageAction)
        widget = dectate.directive(WidgetAction)

    yield app


@pytest.fixture()
def kaybee_settings():
    class KaybeeSettings(BaseModel):
        debugdumper: DebugdumperModel = DebugdumperModel()
        plugins_dir = ''

    yield KaybeeSettings()


@pytest.fixture()
def sphinx_config(kaybee_settings):
    class SphinxConfig:
        def __init__(self):
            self.kaybee_settings = kaybee_settings

    yield SphinxConfig()


@pytest.fixture()
def sphinx_app(sphinx_config, html_builder):
    class SphinxApp:
        def __init__(self):
            self.config = sphinx_config
            self.builder = html_builder
            self.confdir = ''

        def add_config_value(self, *args):
            pass

        def add_directive(self, *args):
            pass

        def connect(self, event_name, some_callable):
            pass

    app: Sphinx = SphinxApp()
    yield app


@pytest.fixture()
def sphinx_env(sphinx_app, sphinx_config):
    class SphinxEnv:
        def __init__(self):
            self.config = sphinx_config

        app = sphinx_app

    env: BuildEnvironment = SphinxEnv()
    yield env


@pytest.fixture()
def sphinx_doctree():
    dt: doctree = dict()
    yield dt


@pytest.fixture()
def template_bridge():
    """ Fixture for the template bridge """

    class TemplateBridge:
        def __init__(self):
            self.loaders = []

    yield TemplateBridge()


@pytest.fixture()
def html_builder(template_bridge):
    class Builder:
        def __init__(self):
            self.outdir = '/tmp/faker'
            self.templates = template_bridge
            self.globalcontext = dict(flag99='flag99')

    builder: StandaloneHTMLBuilder = Builder()
    yield builder
