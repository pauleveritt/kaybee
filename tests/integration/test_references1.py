import pytest

pytestmark = pytest.mark.sphinx('html', testroot='references1')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestReferences1:

    def test_index(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Indexpage' == h1
        li = page.find('li').contents[0].strip()
        assert 'reference1' == li

        # Let's look at the two types of generated reference links
        refs = page.find_all("a", class_="internal")
        assert 4 == len(refs)  # Includes toctree on
        derived_title = refs[0].find('em').contents[0].strip()
        assert 'Reference 1' == derived_title
        explicit_title = refs[1].find('em').contents[0].strip()
        assert 'Reference 1-ish' == explicit_title


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestReferences1Debug:

    def test_references(self, json_page):
        assert 'references' in json_page
        references = json_page['references']

        # First: The reference reference
        reference = references['values']['reference']
        assert 'reference1' in reference
        assert 'reference1' == reference['reference1']['docname']

        # Let's see on the other side with the source of the reference
        reference1 = json_page['resources']['values']['index']
        assert 'reference1' == reference1['props']['references']['reference'][
            0]

        # Next: The author reference
        author_targets = references['values']['author']
        assert 'author1' in author_targets
        assert 'author1' == author_targets['author1']['docname']

        # Let's see on the other side with the source of the reference
        author1 = json_page['resources']['values']['index']
        assert 'author1' == author1['props']['references']['author'][0]


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestReferences1RegistryDebug:

    def test_references(self, json_page):
        assert 'references' in json_page
        references = json_page['references']
        assert 'config' in references

        # references1 contains one registered handler
        config = references['config']
        v = config['reference']
        assert 'kaybee.plugins.references.reference.Reference' == v

        # one value in references
        values = references['values']
        assert 4 == len(values)
