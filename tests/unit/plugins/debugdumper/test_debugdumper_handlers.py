import datetime
import json

import pytest

from kaybee.plugins.debugdumper.handlers import generate_debug_info

class TestPluginGenerateDebugEvent:
    def test_import(self):
        assert 'generate_debug_info' == generate_debug_info.__name__

    def test_debug_true(self, mocker, debugdumper_kb_app, html_builder,
                        sphinx_env, register_valid_event):
        # Turn on debug
        sphinx_env.app.config.kaybee_settings.debugdumper.use_debug = True

        output_file = mocker.mock_open()
        mocker.patch('builtins.open', output_file, create=True)
        mocker.patch('json.dump')
        generate_debug_info(debugdumper_kb_app, html_builder, sphinx_env)
        actual = json.dump.mock_calls[0][1][0]
        assert isinstance(actual['resource']['published'], datetime.datetime)

    def test_debug_false(self, mocker, debugdumper_kb_app, html_builder,
                         sphinx_env, register_valid_event):
        output_file = mocker.mock_open()
        mocker.patch('builtins.open', output_file, create=True)
        mocker.patch('json.dump')
        generate_debug_info(debugdumper_kb_app, html_builder, sphinx_env)
        assert 0 == len(json.dump.mock_calls)
