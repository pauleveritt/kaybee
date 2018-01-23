import pytest

pytestmark = pytest.mark.sphinx('html', testroot='layout')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestLayout:

    def test_article1(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Custom Layout' == h1
        copyright = page.find(id='copyright').contents[0].strip()
        assert 'Custom Layout' == copyright


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestLayoutDebug:

    def test_settings(self, json_page):
        assert 'layouts' in json_page
        settings = json_page['layouts']
        assert 'config' in settings
        config = settings['config']
        assert 'mylayout1' in config
