import pytest

pytestmark = pytest.mark.sphinx('html', testroot='kitchensink')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
def test_index(page):
    content = page.find('h1').contents[0].strip()
    assert 'Kitchen Sink' == content


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestResourceDebug:

    def test_settings(self, json_page):
        assert 'use_debug' in json_page['settings']['debugdumper']
