import dectate
import pytest

from kaybee.plugins.widgets.handlers import (
    dump_settings,
)


@pytest.fixture()
def valid_registration(kb_app):
    @kb_app.widget('listing')
    def listing1(*args):
        return

    dectate.commit(kb_app)
    yield listing1


class TestWidgetsDumpSettings:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_result(self, kb_app, sphinx_env):
        kb_app.config.widgets = dict()
        sphinx_env.app.widgets = dict()
        result = dump_settings(kb_app, sphinx_env)
        assert 'widgets' in result
