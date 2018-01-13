from kaybee.plugins.widgets.widget import Widget


class TestWidget:
    def test_import(self):
        assert 'Widget' == Widget.__name__

    def test_make_context(self):
        w = Widget('widget1', 'widget1', 'name: w23')
        result = w.make_context(dict(), dict())
        assert None is result
