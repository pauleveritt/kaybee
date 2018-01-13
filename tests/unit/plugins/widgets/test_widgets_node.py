import pytest

from kaybee.plugins.widgets.node import widget


@pytest.fixture()
def dummy_widget():
    w = widget()
    w['ids'] = ['first', 'second']
    yield w


class TestWidgetNode:
    def test_import(self):
        assert 'widget' == widget.__name__

    def test_name(self, dummy_widget):
        assert 'first' == dummy_widget.name

    def test_rtype(self, dummy_widget):
        dummy_widget['names'] = ['name1', 'name2']
        assert 'name1' == dummy_widget.rtype

    def test_no_rtype(self, dummy_widget):
        assert None is dummy_widget.rtype
