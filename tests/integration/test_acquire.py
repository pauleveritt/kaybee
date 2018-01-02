import pytest

pytestmark = pytest.mark.sphinx('html', testroot='acquire')


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestAcquire:

    @pytest.mark.parametrize('docname, template', [
        ('index', 'homepage'),
        ('about', 'article'),
        ('folder1/index', 'folder1_section'),
        ('folder1/about', 'root_article'),
        ('folder1/subfolder2/index', 'subfolder2_section'),
        ('folder1/subfolder2/about', 'root_article'),
    ])
    def test_page(self, json_page, docname, template):
        resources = json_page['resources']['values']
        resource = resources[docname]
        assert template == resource['template']