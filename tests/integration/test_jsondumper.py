import pytest

pytestmark = pytest.mark.sphinx('html', testroot='jsondumper')


@pytest.mark.parametrize('json_page', ['testjsondumper.json', ], indirect=True)
class TestJsondumper:

    def test_testjsondumper(self, json_page):
        assert 'a/b/1' == json_page[0]['docname']
