import datetime
import json

import pytest

from kaybee.plugins.jsondumper.handlers import (
    datetime_handler,
    generate_json_info,
)


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


class TestPluginGenerateDebugEvent:
    def test_import(self):
        assert 'generate_json_info' == generate_json_info.__name__

    def test_debug_true(self, mocker, jsondumper_kb_app, html_builder,
                        sphinx_env, register_valid_event):
        output_file = mocker.mock_open()
        mocker.patch('builtins.open', output_file, create=True)
        mocker.patch('json.dump')
        generate_json_info(jsondumper_kb_app, html_builder, sphinx_env)
        actual = json.dump.mock_calls[0][1][0]
        assert isinstance(actual['resource']['published'], datetime.datetime)
