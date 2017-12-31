import datetime
import json

import dectate
import pytest

from kaybee.plugins.debugdumper.action import DumperAction
from kaybee.plugins.debugdumper.events import (
    datetime_handler,
    generate_debug_info,
)

RESOURCES = 'resources'


@pytest.fixture()
def conflicting_events(kb_app):
    # Omit the "order" to disambiguate
    @kb_app.dumper(RESOURCES)
    def dumpresources1(*args):
        return

    @kb_app.dumper(RESOURCES)
    def dumpresources2(*args):
        return

    yield (dumpresources1, dumpresources2)


@pytest.fixture()
def register_valid_event(kb_app):
    @kb_app.dumper(RESOURCES)
    def handle_event(kb_app=None, sphinx_env=None):
        return dict(
            resource=dict(
                published=datetime.datetime.now()

            )
        )

    dectate.commit(kb_app)
    yield handle_event


class TestPluginDebugDumperDateTime:
    def test_import(self):
        assert 'datetime_handler' == datetime_handler.__name__

    def test_serialize(self):
        then = datetime.datetime(2017, 12, 30, 12, 00, 00)
        result = datetime_handler(then)
        assert '2017-12-30T12:00:00' == result

    def test_not_serializable(self):
        with pytest.raises(TypeError):
            datetime_handler(99999)

    def test_json_dump(self):
        debug_info = dict(
            title='Fake',
            then=datetime.datetime(2017, 12, 30, 12, 00, 00)
        )
        expected = '{"title": "Fake", "then": "2017-12-30T12:00:00"}'
        result = json.dumps(debug_info, default=datetime_handler)
        assert expected == result


class TestPluginDumpers:
    def test_import(self):
        assert 'DumperAction' == DumperAction.__name__

    def test_construction(self, kb_app):
        dectate.commit(kb_app)
        assert True

    def test_identifier_default(self):
        da = DumperAction(RESOURCES)
        assert RESOURCES == da.identifier([])

    def test_identifiers_conflict(self, kb_app, conflicting_events):
        # We provide two handlers for same event without distinguishing
        # by order
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(kb_app)

    def test_get_callbacks(self, kb_app, register_valid_event):
        callbacks = DumperAction.get_callbacks(kb_app)
        assert register_valid_event == callbacks[0]


class TestPluginGenerateDebugEvent:
    def test_import(self):
        assert 'generate_debug_info' == generate_debug_info.__name__

    def test_debug_true(self, mocker, kb_app, html_builder,
                        sphinx_env, register_valid_event):
        # Turn on debug
        sphinx_env.app.config['kaybee_settings'].debugdumper.use_debug = True

        output_file = mocker.mock_open()
        mocker.patch('builtins.open', output_file, create=True)
        mocker.patch('json.dump')
        generate_debug_info(kb_app, html_builder, sphinx_env)
        actual = json.dump.mock_calls[0][1][0]
        assert isinstance(actual['resource']['published'], datetime.datetime)

    def test_debug_false(self, mocker, kb_app, html_builder,
                         sphinx_env, register_valid_event):
        output_file = mocker.mock_open()
        mocker.patch('builtins.open', output_file, create=True)
        mocker.patch('json.dump')
        generate_debug_info(kb_app, html_builder, sphinx_env)
        assert 0 == len(json.dump.mock_calls)
