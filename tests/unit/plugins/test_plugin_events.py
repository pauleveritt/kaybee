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


@pytest.fixture()
def builderinit_event(kb_app):
    @kb_app.event('builder-init', 'somescope')
    def handle_builderinit(kb_app, sphinx_app):
        sphinx_app['flag'] = 987

    yield handle_builderinit


@pytest.fixture()
def purgedoc_event(kb_app):
    @kb_app.event('env-purge-doc', 'somescope')
    def handle_purgedoc(kb_app, sphinx_app, env, docname):
        sphinx_app['flag'] = 876

    yield handle_purgedoc


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

    def test_get_invalid_callback(self, kb_app):
        with pytest.raises(AssertionError):
            EventAction.get_callbacks(kb_app, 'xxx')

    def test_get_no_callbacks(self, kb_app, register_valid_event):
        callbacks = EventAction.get_callbacks(kb_app, 'html-context')
        assert 0 == len(callbacks)

    def test_builder_init(self, kb_app, builderinit_event):
        sphinx_app = dict()
        EventAction.call_builder_init(kb_app, sphinx_app)
        callbacks = EventAction.get_callbacks(kb_app,
                                              'builder-init')
        assert 'handle_builderinit' == callbacks[0].__name__
        assert 987 == sphinx_app['flag']

    def test_purge_doc(self, kb_app, purgedoc_event):
        dectate.commit(kb_app)
        sphinx_app = dict()
        env = dict()
        docname = ''
        EventAction.call_purge_doc(kb_app, sphinx_app, env, docname)
        callbacks = EventAction.get_callbacks(kb_app,
                                              'env-purge-doc')
        assert 'handle_purgedoc' == callbacks[0].__name__
        assert 876 == sphinx_app['flag']
