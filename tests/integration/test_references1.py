import pytest

pytestmark = pytest.mark.sphinx('html', testroot='references1')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestReferences1:

    def test_index(self, page):
        content = page.find('h1').contents[0].strip()
        assert 'Hello World' == content
