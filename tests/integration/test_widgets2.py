import pytest

pytestmark = pytest.mark.sphinx('html', testroot='widgets2')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestWidgets2:

    def test_index(self, page):
        # The genericpage doesn't have an acquire for template, so just use
        h1 = page.find('h1').contents[0].strip()
        assert 'Hello World' == h1

        hello = page.find(id='hello').contents[0].strip()
        assert 'Hello Custom Widget Template' == hello
        docname = page.find(id='resource_docname').contents[0].strip()
        assert 'index' == docname

        another_flag = page.find(id='another_flag').contents[0].strip()
        assert '835' == another_flag
        widget_greeting = page.find(id='widget_greeting').contents[0].strip()
        assert 'widget greeting' == widget_greeting
        resources = page.find(id='resources').contents[0].strip()
        assert 'resource' == resources
        resource = page.find(id='resource').contents[0].strip()
        assert 'index' == resource


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestWidgets2Debug:

    def test_settings(self, json_page):
        assert 'widgets' in json_page
        widgets = json_page['widgets']
        assert 'config' in widgets

        # widgets2 contains one registered handler
        config = widgets['config']
        assert 'listing' in config

        # one value in widgets
        values = widgets['values']
        assert 1 == len(values)
        assert 'index' in values
        index = values['index']
        assert 'index' == index['docname']
        assert 'props' in index
        props = index['props']
        assert None is props['template']
