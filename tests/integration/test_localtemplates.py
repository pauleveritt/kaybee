import pytest

pytestmark = pytest.mark.sphinx('html', testroot='localtemplates')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestLocalTemplates:

    def test_index(self, page):
        content = page.find('p').contents[0].strip()
        assert 'local' == content
