import datetime
import json

import dectate
import pytest

from kaybee.plugins.resources.action import ResourceAction
from kaybee.plugins.resources.handlers import (
    handle_builderinited,
    dump_settings
)


@pytest.fixture()
def conflicting_registrations(kb_app):
    # Omit the "order" to disambiguate
    @kb_app.resource('article')
    def article1(*args):
        return

    @kb_app.resource('article')
    def article2(*args):
        return

    yield (article1, article2)


class TestPluginResourcesAction:
    def test_import(self):
        assert 'ResourceAction' == ResourceAction.__name__

    def test_construction(self, kb_app):
        dectate.commit(kb_app)
        assert True

    def test_identifier_default(self):
        da = ResourceAction('article')
        assert 'article' == da.identifier([])

    def test_identifiers_conflict(self, kb_app, conflicting_registrations):
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(kb_app)


class TestPluginResourcesBuilderInitEvent:
    def test_import(self):
        assert 'handle_builderinited' == handle_builderinited.__name__

    def test_result(self, kb_app, sphinx_app):
        result = handle_builderinited(kb_app, sphinx_app)
        assert None is result


class TestPluginResourcesDumpSettingsEvent:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_result(self, kb_app, sphinx_env):
        result = dump_settings(kb_app, sphinx_env)
        assert 'resources' in result
