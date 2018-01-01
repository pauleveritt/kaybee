import pytest

pytestmark = pytest.mark.sphinx('html', testroot='resourcetype')


# @pytest.mark.parametrize('page', ['index.html', ], indirect=True)
# class TestPage:
#
#     def test_index(self, page):
#         content = page.find('h1').contents[0].strip()
#         assert 'Hello World' == page


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestPageDebug:

    def test_page(self, json_page):
        config = json_page['resources']
        assert 'config' in config
