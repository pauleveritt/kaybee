import dectate
import pytest

from kaybee.plugins.references.action import ReferenceAction


class TestPluginReferencesAction:
    def test_import(self):
        assert 'ReferenceAction' == ReferenceAction.__name__

    def test_construction(self, kb_app):
        dectate.commit(kb_app)
        assert True

    def test_identifier_default(self):
        da = ReferenceAction('listing')
        assert 'listing' == da.identifier([])

    def test_identifiers_conflict(self, kb_app, conflicting_registrations):
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(kb_app)

    def test_get_callbacks(self, kb_app, valid_registration):
        callbacks = ReferenceAction.get_callbacks(kb_app)
        assert valid_registration == callbacks[0]
