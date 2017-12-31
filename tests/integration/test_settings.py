import pytest

pytestmark = pytest.mark.sphinx('html', testroot='resources')


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestResourceDebug:

    def test_settings(self, json_page):
        assert 'use_debug' in json_page['settings']['debugdumper'].keys()
