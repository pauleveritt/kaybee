"""
Test the kaybee.setup function
"""

import pytest

pytestmark = pytest.mark.sphinx('html', testroot='localtemplates')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestHomepage:

    def test_index(self, page):
        content = page.find('p').contents[0].strip()
        assert 'local' == content
