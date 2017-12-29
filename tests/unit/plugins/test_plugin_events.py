import dectate
import pytest

from kaybee.plugins.events import EventAction, SphinxEvent


@pytest.fixture()
def register_valid_event(kb_app):
    @kb_app.event(SphinxEvent.EBRD, 'somescope')
    def handle_event():
        return

    dectate.commit(kb_app)
    yield handle_event


@pytest.fixture()
def builderinit_event(kb_app):
    @kb_app.event(SphinxEvent.BI, 'somescope')
    def handle_builderinit(kb_app, sphinx_app):
        sphinx_app['flag'] = 987

    yield handle_builderinit


@pytest.fixture()
def purgedoc_event(kb_app):
    @kb_app.event(SphinxEvent.EPD, 'somescope')
    def handle_purgedoc(kb_app, sphinx_app, env, docname):
        sphinx_app['flag'] = 876

    yield handle_purgedoc


@pytest.fixture()
def before_read_docs_event(kb_app):
    @kb_app.event(SphinxEvent.EBRD, 'somescope')
    def handle_beforereaddocs(kb_app, sphinx_app, env, docnames):
        sphinx_app['flag'] = 765

    yield handle_beforereaddocs


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
        ea = EventAction(SphinxEvent.EBRD, 'somescope')
        assert SphinxEvent.EBRD == ea.name

    def test_get_callbacks(self, kb_app, register_valid_event):
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.EBRD)
        assert 1 == len(callbacks)

    def test_get_invalid_callback(self, kb_app):
        with pytest.raises(AssertionError):
            EventAction.get_callbacks(kb_app, 'xxx')

    def test_get_no_callbacks(self, kb_app, register_valid_event):
        callbacks = EventAction.get_callbacks(kb_app, SphinxEvent.HC)
        assert 0 == len(callbacks)

    def test_builder_init(self, kb_app, builderinit_event):
        sphinx_app = dict()
        EventAction.call_builder_init(kb_app, sphinx_app)
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.BI)
        assert 'handle_builderinit' == callbacks[0].__name__
        assert 987 == sphinx_app['flag']

    def test_purge_doc(self, kb_app, purgedoc_event):
        dectate.commit(kb_app)
        sphinx_app = dict()
        env = dict()
        docname = ''
        EventAction.call_purge_doc(kb_app, sphinx_app, env, docname)
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.EPD)
        assert 'handle_purgedoc' == callbacks[0].__name__
        assert 876 == sphinx_app['flag']

    def test_before_read_docs(self, kb_app, before_read_docs_event):
        dectate.commit(kb_app)
        sphinx_app = dict()
        env = dict()
        docnames = []
        EventAction.call_env_before_read_docs(kb_app, sphinx_app, env,
                                              docnames)
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.EBRD)
        assert 'handle_beforereaddocs' == callbacks[0].__name__
        assert 765 == sphinx_app['flag']
