import dectate
import pytest

from kaybee.plugins.resources.action import ResourceAction


@pytest.fixture()
def conflicting_registrations(resources_kb_app):
    # Omit the "order" to disambiguate
    @resources_kb_app.resource('article')
    def article1(*args):
        return

    @resources_kb_app.resource('article')
    def article2(*args):
        return

    yield (article1, article2)


@pytest.fixture()
def valid_registration(resources_kb_app):
    @resources_kb_app.resource('article')
    def article1(*args):
        return

    dectate.commit(resources_kb_app)
    yield article1


class TestPluginResourcesAction:
    def test_import(self):
        assert 'ResourceAction' == ResourceAction.__name__

    def test_construction(self, resources_kb_app):
        dectate.commit(resources_kb_app)
        assert True

    def test_identifier_default(self):
        da = ResourceAction('article')
        assert 'article' == da.identifier([])

    def test_identifiers_conflict(self, resources_kb_app, conflicting_registrations):
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(resources_kb_app)

    def test_get_callbacks(self, resources_kb_app, valid_registration):
        callbacks = ResourceAction.get_callbacks(resources_kb_app)
        assert valid_registration == callbacks[0]
