import pytest

pytestmark = pytest.mark.sphinx('html', testroot='settings')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestSettingsPage:

    def test_settings(self, page):
        content = page.find('h1').contents[0].strip()
        assert 'Hello World' == content


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestSettingsDebug:

    def test_settings(self, json_page):
        assert 'use_debug' in json_page['settings']['debugdumper'].keys()
