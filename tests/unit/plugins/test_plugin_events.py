import dectate
import pytest

from kaybee.plugins.events import EventAction


@pytest.fixture()
def register_valid_event(kb_app):
    @kb_app.event('env-before-read-docs', 'somescope')
    def handle_event():
        return

    dectate.commit(kb_app)
    yield handle_event


class TestPluginEvents:
    def test_import(self):
        assert 'EventAction' == EventAction.__name__

    def test_construction(self, kb_app):
        dectate.commit(kb_app)
        assert True

    def test_invalid_event_name(self):
        # The class has a sequence with known Sphinx event names. If
        # you try to register an event that doesn't match, you should
        # get an error.
        with pytest.raises(AssertionError):
            EventAction('xxx', 'somescope')

    def test_valid_event_name(self):
        ea = EventAction('env-before-read-docs', 'somescope')
        assert 'env-before-read-docs' == ea.name

    def test_get_callbacks(self, kb_app, register_valid_event):
        callbacks = EventAction.get_callbacks(kb_app,
                                              'env-before-read-docs')
        assert 1 == len(callbacks)

    def test_get_no_callbacks(self, kb_app, register_valid_event):
        callbacks = EventAction.get_callbacks(kb_app, 'xyzpdg')
        assert 0 == len(callbacks)
