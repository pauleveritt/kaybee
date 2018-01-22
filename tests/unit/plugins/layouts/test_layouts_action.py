import dectate
import pytest

from plugins.layouts.action import LayoutAction


class TestLayoutsAction:
    def test_import(self):
        assert 'LayoutAction' == LayoutAction.__name__

    def test_construction(self, layouts_kb_app):
        dectate.commit(layouts_kb_app)
        assert True

    def test_identifier(self):
        da = LayoutAction('mylayout')
        assert 'mylayout' == da.identifier([])

    def test_missing_identifier(self):
        with pytest.raises(TypeError):
            LayoutAction()

    def test_identifiers_conflict(self, layouts_kb_app, conflicting_layouts):
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(layouts_kb_app)

    def test_identifiers_valid(self, layouts_kb_app, valid_layouts):
        assert 'Layout1' == valid_layouts[0].__name__

    def test_get_layout(self, layouts_kb_app, valid_layouts):
        klass = LayoutAction.get_layout(layouts_kb_app, 'mylayout1')
        assert valid_layouts[0] == klass

    def test_invalid_get_layout(self, layouts_kb_app, valid_layouts):
        with pytest.raises(KeyError):
            LayoutAction.get_layout(layouts_kb_app, 'xyzpdq')

    def test_get_callbacks(self, layouts_kb_app, valid_layouts):
        callbacks = LayoutAction.get_callbacks(layouts_kb_app)
        assert valid_layouts[0] == callbacks[0]
