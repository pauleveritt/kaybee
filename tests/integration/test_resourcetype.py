import pytest

pytestmark = pytest.mark.sphinx('html', testroot='resourcetype')


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestPageDebug:

    def test_page(self, json_page):
        resources = json_page['resources']
        r = 'kaybee.plugins.resources.resource.Resource'
        assert dict(resource=r) == resources['config']
        r1 = resources['values']['index']
        assert 'index' == r1['docname']