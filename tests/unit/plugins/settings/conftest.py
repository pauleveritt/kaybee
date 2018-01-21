import dectate
import pytest


@pytest.fixture()
def settings_kb_app():
    class settings_kb_app(dectate.App):
        pass

    yield settings_kb_app
