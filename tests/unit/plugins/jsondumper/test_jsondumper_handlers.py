import datetime
import json

from kaybee.plugins.jsondumper.handlers import (
    generate_json_info,
)


class TestPluginGenerateDebugEvent:
    def test_import(self):
        assert 'generate_json_info' == generate_json_info.__name__

    def test_generate_output(self, mocker, jsondumper_kb_app, html_builder,
                             sphinx_env, register_valid_event):
        output_file = mocker.mock_open()
        mocker.patch('builtins.open', output_file, create=True)
        mocker.patch('json.dump')
        generate_json_info(jsondumper_kb_app, html_builder, sphinx_env)

        # Test the filename written to
        filename = open.mock_calls[0][1][0]
        assert '/tmp/faker/unittest_results.json' == filename

        # Now test the results
        results = json.dump.mock_calls[0][1][0]
        first = results[0]
        assert isinstance(first['published'], datetime.datetime)
