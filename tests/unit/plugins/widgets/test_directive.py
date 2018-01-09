from kaybee.plugins.widgets.directive import BaseWidgetDirective


class TestBaseWidgetDirective:
    def test_import(self):
        assert 'BaseWidgetDirective' == BaseWidgetDirective.__name__
