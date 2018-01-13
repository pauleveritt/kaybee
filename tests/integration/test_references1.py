import pytest

pytestmark = pytest.mark.sphinx('html', testroot='references1')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestReferences1:

    def test_index(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Indexpage' == h1
        li = page.find('li').contents[0].strip()
        assert 'category1' == li


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestReferences1Debug:

    def test_settings(self, json_page):
        assert 'references' in json_page
        references = json_page['references']
        assert 'config' in references

        # references1 contains one registered handler
        config = references['config']
        v = config['category']
        assert 'kaybee.plugins.references.reference.Category' == v

        # one value in references
        values = references['values']
        assert 1 == len(values)
        assert 'category' in values
        category = values['category']
        assert 'category1' in category
        assert 'category1' == category['category1']['docname']

        # Let's see on the other side with the source of the reference
        resource = json_page['resources']['values']['index']
        assert 'category1' == resource['props']['category'][0]
