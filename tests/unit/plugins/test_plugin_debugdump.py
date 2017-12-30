import datetime
import json

import pytest

from kaybee.plugins.debugdumper import datetime_handler


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
