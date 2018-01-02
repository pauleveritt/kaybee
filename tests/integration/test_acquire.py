import pytest

pytestmark = pytest.mark.sphinx('html', testroot='acquire')


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestAcquire:

    @pytest.mark.parametrize('docname, template', [
        ('index', 'resource'),
        ('about', 'resource'),
        ('folder1/index', 'resource'),
        ('folder1/about', 'resource'),
        ('folder1/subfolder2/index', 'resource'),
        ('folder1/subfolder2/about', 'resource'),
    ])
    def test_page(self, json_page, docname, template):
        resources = json_page['resources']['values']
        resource = resources[docname]
        assert template == resource['template']
