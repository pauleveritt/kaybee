import dectate
import pytest

from kaybee.plugins.articles.actions import ToctreeAction


@pytest.fixture()
def conflicting_registrations(articles_kb_app):
    # Omit the "order" to disambiguate
    @articles_kb_app.toctree(context='section')
    def toctree1(*args):
        return

    @articles_kb_app.toctree(context='section')
    def toctree2(*args):
        return

    yield (toctree1, toctree2)


@pytest.fixture()
def two_registrations(articles_kb_app):
    # Omit the "order" to disambiguate
    @articles_kb_app.toctree()
    def toctree1(*args):
        return

    @articles_kb_app.toctree(context='section')
    def toctree2(*args):
        return

    dectate.commit(articles_kb_app)
    yield (toctree1, toctree2)


@pytest.fixture()
def first_default_registrations(articles_kb_app):
    # Omit the "order" to disambiguate
    @articles_kb_app.toctree()
    def toctree1(*args):
        return

    @articles_kb_app.toctree(system_order=50)
    def toctree2(*args):
        return

    @articles_kb_app.toctree(system_order=40)
    def toctree3(*args):
        return

    dectate.commit(articles_kb_app)
    yield (toctree1, toctree2, toctree3)


@pytest.fixture()
def ordered_registrations(articles_kb_app):
    # Omit the "order" to disambiguate
    @articles_kb_app.toctree()
    def toctree1(*args):
        return

    @articles_kb_app.toctree(context='section')
    def toctree2(*args):
        return

    dectate.commit(articles_kb_app)
    yield (toctree1, toctree2)


@pytest.fixture()
def default_registration(articles_kb_app):
    @articles_kb_app.toctree()
    def toctree1(*args):
        return

    dectate.commit(articles_kb_app)
    yield toctree1


@pytest.fixture()
def named_registration(articles_kb_app):
    @articles_kb_app.toctree(context='section')
    def toctree1(*args):
        return

    dectate.commit(articles_kb_app)
    yield toctree1


class TestPluginToctreeAction:
    def test_import(self):
        assert 'ToctreeAction' == ToctreeAction.__name__

    def test_identifier_default(self):
        tt = ToctreeAction()
        assert 'None-80' == tt.identifier([])

    def test_identifier_context(self):
        tt = ToctreeAction('article')
        assert 'article-80' == tt.identifier([])
        assert 'article' == tt.context
        assert 80 == tt.system_order

    def test_identifiers_conflict(self, articles_kb_app, conflicting_registrations):
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(articles_kb_app)

    def test_get_callbacks(self, articles_kb_app, named_registration):
        callbacks = ToctreeAction.get_callbacks(articles_kb_app)
        assert named_registration == callbacks[0]

    def test_get_default(self, articles_kb_app, two_registrations):
        result = ToctreeAction.get_for_context(articles_kb_app)
        expected = two_registrations[0]
        assert expected == result

    def test_get_context(self, articles_kb_app, two_registrations):
        result = ToctreeAction.get_for_context(articles_kb_app, context='section')
        expected = two_registrations[1]
        assert expected == result

    def test_get_default_context(self, articles_kb_app, first_default_registrations):
        # Two registrations on None, get lower system_order
        result = ToctreeAction.get_for_context(articles_kb_app)
        expected = first_default_registrations[2]
        assert expected == result
