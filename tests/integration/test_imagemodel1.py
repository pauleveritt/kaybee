from pathlib import Path

import pytest

pytestmark = pytest.mark.sphinx('html', testroot='imagemodel1')


@pytest.mark.parametrize('page', ['article1.html', ], indirect=True)
class TestImageModels1:

    def test_article1(self, page, content):
        p = Path(content.outdir, 'unittest.png')
        assert p.exists()
        h1 = page.find('h1').contents[0].strip()
        assert 'Article 1' == h1

        usage = page.find(class_='kb-images-usage').contents[0].strip()
        assert 'teaser' == usage
