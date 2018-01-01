import pytest

pytestmark = pytest.mark.sphinx('html', testroot='sphinxapp')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestSphinxApp:

    def test_index(self, page):
        content = page.find('p').contents[0].strip()
        assert 'html' == content
