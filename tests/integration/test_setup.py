"""
Test the kaybee.setup function
"""

import pytest

pytestmark = pytest.mark.sphinx('html', testroot='setup')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestHomepage:

    def test_postrenderer(self, page):
        content = page.find('h1').contents[0].strip()
        assert 'Hello World' == content
