import pytest

pytestmark = pytest.mark.sphinx('html', testroot='jsondumper')


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestJsondumper:

    def test_testjsondumper(self, json_page):
        assert '2017' in json_page['then']
