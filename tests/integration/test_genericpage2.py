import pytest

pytestmark = pytest.mark.sphinx('html', testroot='genericpage2')


@pytest.mark.parametrize('page', ['about.html', ], indirect=True)
class TestGenericpage2:

    def test_about(self, page):
        # The root's acquireds has a genericpage: template pointing to
        # acquired_genericpage. The _templates dir has a
        # acquired_genericpage.html template. We should match in that.
        content = page.find('h1').contents[0].strip()
        assert 'Using acquired_genericpage' == content

        # Ensure that the template has access to genericpage
        p = page.find('p').contents[0].strip()
        assert 'Template name: acquired_genericpage' == p


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestGenericpage2Debug:
    # Get template from the acquireds -> genericpage

    def test_settings(self, json_page):
        assert 'genericpages' in json_page
        genericpages = json_page['genericpages']
        assert 'config' in genericpages

        # genericpage2 contains no registered handlers
        config = genericpages['config']
        assert {} == config

        # one value in genericpage, the 'about' document
        values = genericpages['values']
        assert 1 == len(values)
        assert 'about' in values
        about = values['about']
        assert 'about' == about['docname']
        assert 'acquired_genericpage' == about['template']
