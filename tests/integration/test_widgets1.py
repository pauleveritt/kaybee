import pytest

pytestmark = pytest.mark.sphinx('html', testroot='genericpage1')


@pytest.mark.parametrize('page', ['about.html', ], indirect=True)
class TestGenericpage1:

    def test_about(self, page):
        # The genericpage doesn't have an acquire for template, so just use
        # the normal page.html, which puts the doc title in the <h1>
        content = page.find('h1').contents[0].strip()
        assert 'About' == content


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestGenericpage1Debug:

    def test_settings(self, json_page):
        assert 'genericpages' in json_page
        genericpages = json_page['genericpages']
        assert 'config' in genericpages

        # genericpage1 contains no registered handlers
        config = genericpages['config']
        assert {} == config

        # one value in genericpage
        values = genericpages['values']
        assert 1 == len(values)
        assert 'about' in values
        about = values['about']
        assert 'about' == about['docname']
        assert 'page' == about['template']
