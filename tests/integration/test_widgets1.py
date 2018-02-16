import pytest

pytestmark = pytest.mark.sphinx('html', testroot='widgets1')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestWidgets1:

    def test_widgets1(self, page):
        # The genericpage doesn't have an acquire for template, so just use
        h1 = page.find('h1').contents[0].strip()
        assert 'Hello World' == h1

        hello = page.find(id='hello').contents[0].strip()
        assert 'Hello Custom Widget Template' == hello
        docname = page.find(id='resource_docname').contents[0].strip()
        assert 'index' == docname

    def test_widgets2(self, page):
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

        # widgets1 contains one registered handler, skip any registered
        config = widgets['config']
        assert 'videoplayer' in config

        # one value in widgets
        values = widgets['values']
        assert 2 == len(values)
        assert 'index-widgets1hello' in values
        assert 'index-widgets2hello' in values
        index = values['index-widgets1hello']
        assert 'index' == index['docname']
        assert 'props' in index
        props = index['props']
        assert 'widgets1_hello' == props['template']
