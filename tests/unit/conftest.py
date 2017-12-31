import dectate
import pytest
from docutils.readers import doctree
from pydantic import BaseModel
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.plugins.debugdumper.action import DumperAction
from kaybee.plugins.debugdumper.model import DebugdumperModel
from kaybee.plugins.events import EventAction


@pytest.fixture()
def kb_app():
    class app(dectate.App):
        event = dectate.directive(EventAction)
        dumper = dectate.directive(DumperAction)

    yield app


@pytest.fixture()
def kaybee_settings():
    class KaybeeSettings(BaseModel):
        debugdumper: DebugdumperModel = DebugdumperModel()

    yield KaybeeSettings()


@pytest.fixture()
def sphinx_app(kaybee_settings):
    class SphinxApp:
        def __init__(self):
            self.config = dict(
                kaybee_settings=kaybee_settings
            )

        def add_config_value(self, *args):
            pass

        def connect(self, event_name, callable):
            pass

    app: Sphinx = SphinxApp()
    yield app


@pytest.fixture()
def sphinx_env(sphinx_app):
    class SphinxEnv:
        app = sphinx_app

    env: BuildEnvironment = SphinxEnv()
    yield env


@pytest.fixture()
def sphinx_doctree():
    dt: doctree = dict()
    yield dt


@pytest.fixture()
def html_builder():
    class Builder:
        outdir = '/tmp/faker'

    builder: StandaloneHTMLBuilder = Builder()
    yield builder
