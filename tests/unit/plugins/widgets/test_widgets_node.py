from kaybee.plugins.widgets.node import widget


class TestWidgetNode:

    def test_import(self):
        assert widget.__name__ == 'widget'
