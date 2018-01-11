import pytest

pytestmark = pytest.mark.sphinx('html', testroot='widgets1')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestWidgets1:

    def test_index(self, page):
        # The genericpage doesn't have an acquire for template, so just use
        h1 = page.find('h1').contents[0].strip()
        assert 'Hello World' == h1

        hello = page.find(id='hello').contents[0].strip()
        assert 'Hello Custom Widget Template' == hello
        docname = page.find(id='resource_docname').contents[0].strip()
        assert 'index' == docname


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestWidgets1Debug:

    def test_settings(self, json_page):
        assert 'widgets' in json_page
        widgets = json_page['widgets']
        assert 'config' in widgets

        # widgets1 contains one registered handler
        config = widgets['config']
        assert {'widget': 'kaybee.plugins.widgets.widget.Widget'} == config

        # one value in widgets
        values = widgets['values']
        assert 1 == len(values)
        assert 'index' in values
        index = values['index']
        assert 'index' == index['docname']
        assert 'props' in index
        props = index['props']
        assert 'widgets1_hello' == props['template']
