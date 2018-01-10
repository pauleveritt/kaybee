import dectate
import pytest

from kaybee.plugins.widgets.action import WidgetAction


@pytest.fixture()
def conflicting_registrations(kb_app):
    # Omit the "order" to disambiguate
    @kb_app.widget('listing')
    def listing1(*args):
        return

    @kb_app.widget('listing')
    def listing2(*args):
        return

    yield (listing1, listing2)


@pytest.fixture()
def valid_registration(kb_app):
    @kb_app.widget('listing')
    def listing1(*args):
        return

    dectate.commit(kb_app)
    yield listing1


class TestPluginWidgetsAction:
    def test_import(self):
        assert 'WidgetAction' == WidgetAction.__name__

    def test_construction(self, kb_app):
        dectate.commit(kb_app)
        assert True

    def test_identifier_default(self):
        da = WidgetAction('listing')
        assert 'listing' == da.identifier([])

    def test_identifiers_conflict(self, kb_app, conflicting_registrations):
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(kb_app)

    def test_get_callbacks(self, kb_app, valid_registration):
        callbacks = WidgetAction.get_callbacks(kb_app)
        assert valid_registration == callbacks[0]
