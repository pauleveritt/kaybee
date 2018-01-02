import pytest

pytestmark = pytest.mark.sphinx('html', testroot='debugdumper')


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestDebugDumper:

    def test_testdumper(self, json_page):
        assert '2017' in json_page['then']
