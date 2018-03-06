import pytest

pytestmark = pytest.mark.sphinx('html', testroot='articles1')


@pytest.mark.parametrize('page', ['articles/article1.html', ], indirect=True)
class TestArticles1:

    def test_article1(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Article 1' == h1

        # Author listing
        authors = page.find(id='kb-author-listing').find_all('li')
        assert 2 == len(authors)
        author1 = authors[0].find('a').contents[0].strip()
        assert 'Author 1' == author1

        # Categories listing
        categories = page.find(id='kb-category-listing').find_all('li')
        assert 2 == len(categories)
        category1 = categories[0].find('a').contents[0].strip()
        assert 'Category 2' == category1


@pytest.mark.parametrize('page', ['authors/author1.html', ],
                         indirect=True)
class TestAuthor1:

    def test_author1(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Author 1' == h1

        items = [i.contents[0].strip()
                 for i in page.find_all(class_='kb-reference-item')]
        assert 2 == len(items)
        assert 'Article 1' in items


@pytest.mark.parametrize('page', ['categories/category2.html', ],
                         indirect=True)
class TestCategories2:

    def test_article2(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Category 2' == h1

        items = [i.contents[0].strip()
                 for i in page.find_all(class_='kb-reference-item')]
        assert 2 == len(items)
        assert 'Article 1' in items


@pytest.mark.parametrize('page', ['articles/article2.html', ],
                         indirect=True)
class TestQuerylist:

    def test_querylist(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Article 2' == h1

        labels = [
            result.contents[0].strip()
            for result in page.find_all(class_='kb-querylist-label')]
        items = [
            result.contents[0].strip()
            for result in page.find_all(class_='kb-querylist-item')]
        assert 2 == len(labels)
        assert 'Recent Blog Posts' in labels
        assert 6 == len(items)
        assert 'Section 1' in items


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
        assert '' == homepage['section']
        assert 'articles/index' in homepage['toctree']
        assert None is homepage['series']

        # articles
        articles = resource_values['articles/index']
        assert 'articles/index' == articles['docname']
        assert 'Articles' == articles['title']
        assert '' == articles['section']
        assert None is articles['series']

        # article1
        article1 = resource_values['articles/article1']
        assert 'articles/article1' == article1['docname']
        assert 'Article 1' == article1['title']
        assert 'articles/index' == article1['section']
        assert [] == article1['toctree']
        assert 3 == len(article1['series'])

        # section1
        section1 = resource_values['section1/index']
        assert 'section1/index' == section1['docname']
        assert 'Section 1' == section1['title']
        assert '' == section1['section']
        assert ['section1/article2'] == section1['toctree']
        assert 'section1/article2' == section1['get_featured_resource']
