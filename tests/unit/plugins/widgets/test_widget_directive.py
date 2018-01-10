from kaybee.plugins.widgets.directive import WidgetDirective
from kaybee import app


class TestWidgetDirective:
    def test_import(self):
        assert 'WidgetDirective' == WidgetDirective.__name__

    def test_construction(self, dummy_directive):
        assert 'dummy_directive' == dummy_directive.name

    def test_get_widget_class(self, monkeypatch,
                              dummy_directive_class,
                              dummy_widget_class,
                              kb_app):
        # Setup fake registry
        monkeypatch.setattr(app, 'kb', kb_app)
        dwc = dummy_directive_class.name
        kb_app.config.widgets = {dwc: dummy_widget_class}

        actual = WidgetDirective.get_widget_class(dwc)
        assert dummy_widget_class == actual

    def test_get_widget(self, monkeypatch, dummy_directive,
                        dummy_directive_class,
                        dummy_widget_class,
                        kb_app):
        monkeypatch.setattr(app, 'kb', kb_app)
        dwc = dummy_directive_class.name
        kb_app.config.widgets = {dwc: dummy_widget_class}

        actual = WidgetDirective.get_widget_class(dwc)
        assert dummy_widget_class == actual
        widget = dummy_directive.get_widget('dummy123')
        assert 'dummy123' == widget.docname
        assert 'dummy_directive' == widget.rtype

    def test_docname(self, dummy_directive):
        assert 'somedoc' == dummy_directive.docname

    def test_widgets(self, dummy_directive):
        assert dict() == dummy_directive.widgets

    def test_run_result(self, monkeypatch,
                        dummy_directive_class,
                        dummy_widget_class,
                        dummy_directive, kb_app):
        # Setup fake registry
        monkeypatch.setattr(app, 'kb', kb_app)
        drc = dummy_directive_class.name
        kb_app.config.widgets = {drc: dummy_widget_class}

        result = dummy_directive.run()
        assert 'widget' == result[0].__class__.__name__
