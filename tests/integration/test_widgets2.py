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

        listing_flag = page.find(id='listing_flag').contents[0].strip()
        assert '98' == listing_flag
        another_flag = page.find(id='another_flag').contents[0].strip()
        assert '835' == another_flag
        widget_content = str(page.find(id='widget_content'))
        assert '<p>Here is some <em>more</em> text.</p>' in widget_content
        widget_greeting = page.find(id='widget_greeting').contents[0].strip()
        assert 'widget greeting' == widget_greeting
        resources = page.find(id='resources').contents[0].strip()
        assert 'resource' == resources
        resource = page.find(id='resource').contents[0].strip()
        assert 'index' == resource

        # Querylist
        ql = page.find(id='querylist-ql1')
        ql_results = ql.find_all('ul')[1].find_all('li')
        assert 1 == len(ql_results)

        # Sectionquery
        ql = page.find(id='sectionquery-sectionquery1')
        ql_results = ql.find_all('ul')[0].find_all('li')
        assert 2 == len(ql_results)


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
        assert 3 == len(values)
        assert 'index-widgets1hello' in values
        index = values['index-widgets1hello']
        assert 'index' == index['docname']
        assert 'props' in index
        props = index['props']
        assert None is props['template']
