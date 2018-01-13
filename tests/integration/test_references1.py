import pytest

pytestmark = pytest.mark.sphinx('html', testroot='references1')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestReferences1:

    def test_index(self, page):
        content = page.find('h1').contents[0].strip()
        assert 'Hello World' == content


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestReferences1Debug:

    def test_settings(self, json_page):
        assert 'references' in json_page
        references = json_page['references']
        assert 'config' in references

        # references1 contains one registered handler
        config = references['config']
        assert {'reference': 'kaybee.plugins.widgets.widget.Widget'} == config
        return

        # one value in widgets
        values = widgets['values']
        assert 1 == len(values)
        assert 'index' in values
        index = values['index']
        assert 'index' == index['docname']
        assert 'props' in index
        props = index['props']
        assert 'widgets1_hello' == props['template']
