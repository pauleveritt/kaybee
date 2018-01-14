import pytest

pytestmark = pytest.mark.sphinx('html', testroot='toctrees1')


@pytest.mark.parametrize('page', ['article1.html', ], indirect=True)
class TestToctrees1:

    def test_article1(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Custom Article' == h1


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestToctrees1Debug:

    def test_settings(self, json_page):
        resources = json_page['resources']
        assert 'config' in resources

        # article/section/homepage is in the registered handlers
        resources_config = resources['config']
        assert 'article' in resources_config
        assert 'homepage' in resources_config
        assert 'section' in resources_config

        # toctrees are registered (built-in and one custom)
        toctrees = json_page['toctrees']
        toctrees_config = toctrees['config']
        assert 'None-80' in toctrees_config
        assert 'None-40' in toctrees_config
        assert 'Toctree' in toctrees_config['None-80']
