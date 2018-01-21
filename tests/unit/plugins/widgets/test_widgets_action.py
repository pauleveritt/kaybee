import dectate
import pytest

from kaybee.plugins.widgets.action import WidgetAction


@pytest.fixture()
def conflicting_registrations(widgets_kb_app):
    # Omit the "order" to disambiguate
    @widgets_kb_app.widget('listing')
    def listing1(*args):
        return

    @widgets_kb_app.widget('listing')
    def listing2(*args):
        return

    yield (listing1, listing2)


@pytest.fixture()
def valid_registration(widgets_kb_app):
    @widgets_kb_app.widget('listing')
    def listing1(*args):
        return

    dectate.commit(widgets_kb_app)
    yield listing1


class TestPluginWidgetsAction:
    def test_import(self):
        assert 'WidgetAction' == WidgetAction.__name__

    def test_construction(self, widgets_kb_app):
        dectate.commit(widgets_kb_app)
        assert True

    def test_identifier_default(self):
        da = WidgetAction('listing')
        assert 'listing' == da.identifier([])

    def test_identifiers_conflict(self, widgets_kb_app, conflicting_registrations):
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(widgets_kb_app)

    def test_get_callbacks(self, widgets_kb_app, valid_registration):
        callbacks = WidgetAction.get_callbacks(widgets_kb_app)
        assert valid_registration == callbacks[0]
