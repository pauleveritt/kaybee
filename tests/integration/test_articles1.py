import pytest

pytestmark = pytest.mark.sphinx('html', testroot='articles1')


@pytest.mark.parametrize('page', ['article1.html', ], indirect=True)
class TestArticles1:

    def test_article1(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Custom Article' == h1


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestArticles1Debug:

    def test_settings(self, json_page):
        resources = json_page['resources']
        assert 'config' in resources

        # article/section/homepage is in the registered handlers
        resources_config = resources['config']
        assert 'article' in resources_config
        assert 'homepage' in resources_config
        assert 'section' in resources_config

        # Test some values
        resource_values = resources['values']

        # homepage
        homepage = resource_values['index']
        assert 'index' == homepage['docname']
        assert 'Hello World' == homepage['title']
        assert None == homepage['excerpt']
        assert '' == homepage['section']
        assert ['article1', 'section1/index'] == homepage['toctree']
        assert None is homepage['series']

        # article1
        article1 = resource_values['article1']
        assert 'article1' == article1['docname']
        assert 'Article 1' == article1['title']
        assert None == article1['excerpt']
        assert '' == article1['section']
        assert [] == article1['toctree']
        assert 2 == len(article1['series'])

        # section1
        section1 = resource_values['section1/index']
        assert 'section1/index' == section1['docname']
        assert 'Section 1' == section1['title']
        assert None == section1['excerpt']
        assert '' == section1['section']
        assert ['section1/article2'] == section1['toctree']
        assert 'article1' == section1['series'][0]['docname']
        assert 'section1/article2' == section1['get_featured_resource']
