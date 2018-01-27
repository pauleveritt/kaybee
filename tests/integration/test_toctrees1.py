import pytest

pytestmark = pytest.mark.sphinx('html', testroot='toctrees1')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestToctrees1:

    def test_index(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Custom Homepage' == h1

        entries = page.find_all("a", class_="reference")
        assert 2 == len(entries)
        assert 'article1.html' == entries[0].attrs['href'].strip()
        assert 'section1/index.html' == entries[1].attrs['href'].strip()


@pytest.mark.parametrize('page', ['section1/index.html', ], indirect=True)
class TestToctrees1:

    def test_section1(self, page):
        div = page.find(id='first_toctree_title').contents[0].strip()
        # The resource only knows about the docname in the toctree. The
        # article.series is what converts to resources.
        assert 'section1/article2' == div


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
        assert 'None-70' in toctrees_config
        assert 'Toctree' in toctrees_config['None-70']
