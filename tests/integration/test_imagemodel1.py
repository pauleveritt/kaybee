import pytest

pytestmark = pytest.mark.sphinx('html', testroot='imagemodel1')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestImageModels1:

    def test_article1(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Hello World' == h1

        h3 = page.find(class_='kb-images-heading')
        assert None is h3


@pytest.mark.parametrize('page', ['article1.html', ], indirect=True)
class TestImageModels2:

    def test_article1(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Article 1' == h1

        h3 = page.find(class_='kb-images-heading').contents[0].strip()
        assert 'Attached Images' == h3
