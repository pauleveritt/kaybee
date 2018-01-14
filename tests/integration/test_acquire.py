import pytest

pytestmark = pytest.mark.sphinx('html', testroot='acquire')


@pytest.mark.parametrize('page', ['folder1/about.html', ], indirect=True)
class TestAcquire:

    def test_about(self, page):
        # First, make sure we are in the right place
        h1 = page.find('h1').contents[0].strip()
        assert 'Root Article' == h1

        # Test that resource.acquire worked
        template = page.find(id='template').contents[0].strip()
        assert 'Acquire: root_article' == template
        flag = page.find(id='flag').contents[0].strip()
        assert 'Acquire: 99' == flag


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestAcquireDebug:

    @pytest.mark.parametrize('docname, template', [
        ('index', 'aqhomepage'),
        ('about', 'aqarticle'),
        ('folder1/index', 'folder1_section'),
        ('folder1/about', 'root_article'),
        ('folder1/subfolder2/index', 'subfolder2_section'),
        ('folder1/subfolder2/about', 'root_article'),
    ])
    def test_page(self, json_page, docname, template):
        resources = json_page['resources']['values']
        resource = resources[docname]
        assert template == resource['template']
