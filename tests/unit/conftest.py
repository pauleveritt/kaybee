import dectate
import pytest

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

    app = SphinxApp()
    yield app
