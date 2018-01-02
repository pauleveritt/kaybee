import pytest

pytestmark = pytest.mark.sphinx('html', testroot='resourcetype')


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestResourceTypeDebug:

    @pytest.mark.parametrize('docname, parents', [
        ('index', []),
        ('about', ['index']),
        ('folder1/index', ['index']),
        ('folder1/about', ['folder1/index', 'index']),
        ('folder1/subfolder2/index', ['folder1/index', 'index']),
        ('folder1/subfolder2/about',
         ['folder1/subfolder2/index', 'folder1/index', 'index']),
    ])
    def test_page(self, json_page, docname, parents):
        resources = json_page['resources']
        r = 'kaybee.plugins.resources.resource.Resource'

        # Check the config
        assert dict(resource=r) == resources['config']

        # Now values
        v = resources['values']
        assert 6 == len(v.values())
        assert docname == v[docname]['docname']

        # Now the custom debugdumper for this test root which serializes
        # parents and repr
        doc = json_page['testing'][docname]
        assert parents == doc['parent_docnames']
        assert docname == doc['repr']
