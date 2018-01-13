import pytest

pytestmark = pytest.mark.sphinx('html', testroot='resources')


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestResourceDebug:

    def test_settings(self, json_page):
        assert 'resources' in json_page
        settings = json_page['resources']
        assert 'config' in settings
        assert 'values' in settings

        # Inspect some details from a value
        index = settings['values']['index']
        assert 'index' == index['docname']
        assert 'Hello World' == index['title']
        assert 'page' == index['template']
        assert 'resource' == index['rtype']
        assert None is index['parent']
        assert 'index' == index['repr']
