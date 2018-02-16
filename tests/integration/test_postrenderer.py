import pytest

pytestmark = pytest.mark.sphinx('html', testroot='postrenderer')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestPostrenderer:

    def test_prindex(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'HELLO WORLD' == h1
