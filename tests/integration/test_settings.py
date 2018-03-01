import pytest

pytestmark = pytest.mark.sphinx('html', testroot='settings')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestSettingsIndex:

    def test_index(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Settings Template' == h1
        div = page.find('div').contents[0].strip()
        assert 'True' == div


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestSettingsDebug:

    def test_settings(self, json_page):
        assert 'use_debug' in json_page['settings']['debugdumper']
