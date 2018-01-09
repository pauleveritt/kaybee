from kaybee.plugins.widgets.base_widget import BaseWidget


class TestBaseWidget:
    def test_import(self):
        assert 'BaseWidget' == BaseWidget.__name__
