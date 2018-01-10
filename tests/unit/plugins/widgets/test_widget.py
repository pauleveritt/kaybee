from kaybee.plugins.widgets.widget import Widget


class TestWidget:
    def test_import(self):
        assert 'Widget' == Widget.__name__
