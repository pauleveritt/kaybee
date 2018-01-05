import pytest

pytestmark = pytest.mark.sphinx('html', testroot='genericpage3')


@pytest.mark.parametrize('page', ['about.html', ], indirect=True)
class TestGenericpage3:

    def test_about(self, page):
        # The root's acquireds has a all: template pointing to
        # acquired_all. The _templates dir has a
        # acquired_all.html template. We should match in that.
        content = page.find('h1').contents[0].strip()
        assert 'Using acquired_all' == content


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestGenericpage3Debug:
    # Get template from the acquireds -> genericpage

    def test_settings(self, json_page):
        assert 'genericpages' in json_page
        genericpages = json_page['genericpages']
        assert 'config' in genericpages

        # genericpage1 contains no registered handlers
        config = genericpages['config']
        assert {} == config

        # one value in genericpage, the 'about' document
        values = genericpages['values']
        assert 1 == len(values)
        assert 'about' in values
        about = values['about']
        assert 'about' == about['docname']
        assert 'acquired_all' == about['template']
