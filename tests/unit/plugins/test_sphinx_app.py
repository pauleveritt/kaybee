from kaybee.plugins.sphinx_app.handlers import (
    sphinx_app_html_context,
)


class TestPluginSphinxAppHandlers:
    def test_import(self):
        assert 'sphinx_app_html_context' == sphinx_app_html_context.__name__

    def test_handler(self, kb_app, sphinx_app):
        context = dict()
        sphinx_app_html_context(kb_app, sphinx_app,
                                '', '', context, dict())
        assert 'sphinx_app' in context
