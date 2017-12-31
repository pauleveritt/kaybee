import dectate
import pytest

from kaybee.plugins.events import EventAction, SphinxEvent

import importlib
import importscan


@pytest.fixture()
def register_valid_event(kb_app):
    @kb_app.event(SphinxEvent.EBRD)
    def handle_event():
        return

    dectate.commit(kb_app)
    yield handle_event


@pytest.fixture()
def register_scoped_event(kb_app):
    @kb_app.event(SphinxEvent.EBRD, scope='resources')
    def handle_event():
        return

    dectate.commit(kb_app)
    yield handle_event


@pytest.fixture()
def conflicting_events(kb_app):
    # Omit the "order" to disambiguate
    @kb_app.event(SphinxEvent.HPC)
    def handle_pagecontext1(*args):
        return

    @kb_app.event(SphinxEvent.HPC)
    def handle_pagecontext2(*args):
        return

    yield (handle_pagecontext1, handle_pagecontext2)


@pytest.fixture()
def scoped_conflict_event(kb_app):
    # Omit the "order" to disambiguate
    @kb_app.event(SphinxEvent.HPC, scope='resources')
    def handle_pagecontext1(*args):
        return

    @kb_app.event(SphinxEvent.HPC, scope='resources')
    def handle_pagecontext2(*args):
        return

    yield (handle_pagecontext1, handle_pagecontext2)


@pytest.fixture()
def system_nonconflicting_events(kb_app):
    @kb_app.event(SphinxEvent.HPC, system_order=50)
    def handle_pagecontext1(*args):
        return

    @kb_app.event(SphinxEvent.HPC)
    def handle_pagecontext2(*args):
        return

    yield (handle_pagecontext1, handle_pagecontext2)


@pytest.fixture()
def system_conflicting_events(kb_app):
    @kb_app.event(SphinxEvent.HPC, system_order=50)
    def handle_pagecontext1(*args):
        return

    @kb_app.event(SphinxEvent.HPC, system_order=50)
    def handle_pagecontext2(*args):
        return

    yield (handle_pagecontext1, handle_pagecontext2)


@pytest.fixture()
def multiple_events(kb_app):
    @kb_app.event(SphinxEvent.HPC)
    def handle_pagecontext1(*args):
        return

    @kb_app.event(SphinxEvent.HPC, order=10)
    def handle_pagecontext2(*args):
        return

    @kb_app.event(SphinxEvent.HPC, order=9)
    def handle_pagecontext3(*args):
        return

    @kb_app.event(SphinxEvent.HPC, order=90)
    def handle_pagecontext4(*args):
        return

    @kb_app.event(SphinxEvent.BI)
    def handle_builderinit1(*args):
        return

    dectate.commit(kb_app)
    yield (handle_pagecontext1, handle_pagecontext2, handle_pagecontext3,
           handle_pagecontext4)


@pytest.fixture()
def builderinit_event(kb_app):
    @kb_app.event(SphinxEvent.BI)
    def handle_builderinit(*args):
        sphinx_app = args[1]
        sphinx_app.flag = 987

    yield handle_builderinit


@pytest.fixture()
def purgedoc_event(kb_app):
    @kb_app.event(SphinxEvent.EPD)
    def handle_purgedoc(*args):
        sphinx_app = args[1]
        sphinx_app.flag = 876

    yield handle_purgedoc


@pytest.fixture()
def before_read_docs_event(kb_app):
    @kb_app.event(SphinxEvent.EBRD)
    def handle_beforereaddocs(*args):
        sphinx_app = args[1]
        sphinx_app.flag = 765

    yield handle_beforereaddocs


@pytest.fixture()
def doctree_read_event(kb_app):
    @kb_app.event(SphinxEvent.DREAD)
    def handle_doctreeread(*args):
        sphinx_app = args[1]
        sphinx_app.flag = 654

    yield handle_doctreeread


@pytest.fixture()
def doctree_resolved_event(kb_app):
    @kb_app.event(SphinxEvent.DRES)
    def handle_doctreeresolved(*args):
        sphinx_app = args[1]
        sphinx_app.flag = 543

    yield handle_doctreeresolved


@pytest.fixture()
def html_collect_pages_event(kb_app):
    @kb_app.event(SphinxEvent.HCP)
    def handle_collectpages(*args):
        sphinx_app = args[1]
        sphinx_app.flag = 432

    yield handle_collectpages


@pytest.fixture()
def check_consistency_event(kb_app):
    @kb_app.event(SphinxEvent.ECC)
    def handle_checkconsistency(*args):
        builder = args[1]
        builder.flag = 321

    yield handle_checkconsistency


@pytest.fixture()
def missing_reference_event(kb_app):
    @kb_app.event(SphinxEvent.MR)
    def handle_missingreference(*args):
        sphinx_app = args[1]
        sphinx_app.flag = 210

    yield handle_missingreference


@pytest.fixture()
def html_page_context_event(kb_app):
    @kb_app.event(SphinxEvent.HPC)
    def handle_pagecontext(*args):
        sphinx_app = args[1]
        sphinx_app.flag = 123

    yield handle_pagecontext


class TestPluginEvents:
    def test_import(self):
        assert 'EventAction' == EventAction.__name__

    def test_construction(self, kb_app):
        dectate.commit(kb_app)
        assert True

    def test_identifier_default(self):
        ea = EventAction(SphinxEvent.BI)
        assert 'builder-inited-20' == ea.identifier([])

    def test_identifier_order(self):
        ea = EventAction(SphinxEvent.BI, 10)
        assert 'builder-inited-10' == ea.identifier([])

    def test_identifiers_valid(self):
        # We provide two handlers for same event and distinguish
        # using 'order'
        ea1 = EventAction(SphinxEvent.BI)
        ea2 = EventAction(SphinxEvent.BI, 10)
        assert 'builder-inited-20' == ea1.identifier([])

    def test_scoped_identifiers(self):
        # We provide two handlers for same event and distinguish
        # using 'order'
        ea1 = EventAction(SphinxEvent.BI, scope='resources')
        ea2 = EventAction(SphinxEvent.BI, 10)
        assert 'builder-inited-resources-20' == ea1.identifier([])

    def test_identifiers_conflict(self, kb_app, conflicting_events):
        # We provide two handlers for same event without distinguishing
        # by order
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(kb_app)

    def test_system_nonconflict(self, kb_app, system_nonconflicting_events):
        # A system handler won't conflict with a non-system handler
        dectate.commit(kb_app)

    def test_system_conflict(self, kb_app, system_conflicting_events):
        # We provide two handlers for same event without distinguishing
        # by order
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(kb_app)

    def test_scoped_nonconflict(self, kb_app, register_scoped_event):
        # A system handler won't conflict with a non-system handler
        dectate.commit(kb_app)

    def test_scoped_conflict(self, kb_app, scoped_conflict_event):
        # A system handler won't conflict with a non-system handler
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(kb_app)

    def test_invalid_event_name(self):
        # The class has a sequence with known Sphinx event names. If
        # you try to register an event that doesn't match, you should
        # get an error.
        with pytest.raises(AssertionError):
            EventAction('xxx')

    def test_get_callbacks(self, kb_app, register_valid_event):
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.EBRD)
        assert register_valid_event == callbacks[0]

    def test_get_invalid_callback(self, kb_app):
        with pytest.raises(AssertionError):
            # noinspection PyTypeChecker
            EventAction.get_callbacks(kb_app, 'xxx')

    def test_get_no_callbacks(self, kb_app, register_valid_event):
        callbacks = EventAction.get_callbacks(kb_app, SphinxEvent.HPC)
        assert 0 == len(callbacks)
        assert register_valid_event not in callbacks

    def test_multiple_callbacks_sorted(self, kb_app, multiple_events):
        callbacks = EventAction.get_callbacks(kb_app, SphinxEvent.HPC)
        assert len(multiple_events) == len(callbacks)
        assert multiple_events[0] == callbacks[2]
        assert multiple_events[1] == callbacks[1]
        assert multiple_events[2] == callbacks[0]
        assert multiple_events[3] == callbacks[3]

    #
    # Sphinx event handlers
    #

    def test_builder_init(self, monkeypatch, kb_app, sphinx_app, builderinit_event):
        monkeypatch.setattr(importlib, 'import_module', lambda x: None)
        monkeypatch.setattr(importscan, 'scan', lambda x: None)
        EventAction.call_builder_init(kb_app, sphinx_app)
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.BI)
        assert builderinit_event in callbacks
        assert 987 == sphinx_app.flag

    def test_purge_doc(self, kb_app, sphinx_app, sphinx_env, purgedoc_event):
        dectate.commit(kb_app)
        docname = ''
        EventAction.call_purge_doc(kb_app, sphinx_app, sphinx_env, docname)
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.EPD)
        assert purgedoc_event in callbacks
        assert 876 == sphinx_app.flag

    def test_before_read_docs(self, kb_app, sphinx_app, sphinx_env,
                              before_read_docs_event):
        dectate.commit(kb_app)
        docnames = []
        EventAction.call_env_before_read_docs(kb_app, sphinx_app, sphinx_env,
                                              docnames)
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.EBRD)
        assert before_read_docs_event in callbacks
        assert 765 == sphinx_app.flag

    def test_env_doctree_read(self, kb_app, sphinx_app, sphinx_doctree,
                              doctree_read_event):
        dectate.commit(kb_app)
        EventAction.call_env_doctree_read(kb_app, sphinx_app, sphinx_doctree)
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.DREAD)
        assert doctree_read_event in callbacks
        assert 654 == sphinx_app.flag

    def test_doctree_resolved(self, kb_app, sphinx_app, sphinx_doctree,
                              doctree_resolved_event):
        dectate.commit(kb_app)
        fromdocname = ''
        EventAction.call_doctree_resolved(kb_app, sphinx_app, sphinx_doctree,
                                          fromdocname)
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.DRES)
        assert doctree_resolved_event in callbacks
        assert 543 == sphinx_app.flag

    def test_html_collect_pages(self, kb_app, sphinx_app,
                                html_collect_pages_event):
        dectate.commit(kb_app)
        # This is an iterator, call list() on it
        list(EventAction.call_html_collect_pages(kb_app, sphinx_app))
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.HCP)
        assert html_collect_pages_event in callbacks
        assert 432 == sphinx_app.flag

    def test_env_check_consistency(self, kb_app,
                                   sphinx_env,
                                   html_builder,
                                   check_consistency_event):
        dectate.commit(kb_app)
        EventAction.call_env_check_consistency(kb_app, html_builder,
                                               sphinx_env)
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.ECC)
        assert check_consistency_event in callbacks
        assert 321 == html_builder.flag

    def test_missing_reference(self, kb_app, sphinx_app,
                               sphinx_env,
                               missing_reference_event
                               ):
        dectate.commit(kb_app)
        node = object()
        contnode = object()
        EventAction.call_missing_reference(kb_app, sphinx_app,
                                           sphinx_env, node, contnode)
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.MR)
        assert missing_reference_event in callbacks
        assert 210 == sphinx_app.flag

    def test_html_page_context(self, kb_app, sphinx_app,
                               sphinx_doctree,
                               html_page_context_event):
        dectate.commit(kb_app)
        pagename = ''
        templatename = ''
        context = dict()
        EventAction.call_html_page_context(kb_app, sphinx_app,
                                           pagename,
                                           templatename,
                                           context,
                                           sphinx_doctree
                                           )
        callbacks = EventAction.get_callbacks(kb_app,
                                              SphinxEvent.HPC)
        assert html_page_context_event in callbacks
        assert 123 == sphinx_app.flag
