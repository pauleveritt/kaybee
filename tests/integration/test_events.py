import pytest

pytestmark = pytest.mark.sphinx('html', testroot='events')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestEvents:

    def test_events(self, page):
        title = page.find('title').contents[0].strip()
        assert 'index' == title

        bi = page.find(id='bi').contents[0].strip()
        assert 'BI' == bi

        hpc = page.find(id='hpc').contents[0].strip()
        assert 'HPC' == hpc
