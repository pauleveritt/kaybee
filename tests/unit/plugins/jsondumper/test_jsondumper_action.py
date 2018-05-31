import dectate
import pytest

from kaybee.plugins.jsondumper.action import DumperAction


class TestDebugDumperAction:
    def test_import(self):
        assert 'DumperAction' == DumperAction.__name__

    def test_construction(self, jsondumper_kb_app):
        dectate.commit(jsondumper_kb_app)
        assert True

    def test_identifier_default(self):
        da = DumperAction('resources')
        assert 'resources' == da.identifier([])

    def test_identifiers_conflict(self, jsondumper_kb_app,
                                  conflicting_events):
        # We provide two handlers for same event without distinguishing
        # by order
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(jsondumper_kb_app)

    def test_get_callbacks(self, jsondumper_kb_app, register_valid_event):
        callbacks = DumperAction.get_callbacks(jsondumper_kb_app)
        assert register_valid_event == callbacks[0]
