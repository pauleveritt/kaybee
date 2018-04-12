import pytest

from kaybee.plugins.articles.author import Author


@pytest.fixture()
def dummy_author():
    yaml = """
label: author1    
images:
    - usage: icon_24
      filename: paul_headshotx24.jpeg
    """
    yield Author('authors/author1', 'author', yaml)


class TestAuthor:
    def test_import(self):
        assert 'Author' == Author.__name__

    def test_construction(self, dummy_author):
        assert 'authors/author1' == dummy_author.docname

    def test_no_featured_resource(self, dummy_author: Author):
        ht = dummy_author.headshot_thumbnail('icon_24')
        assert 'authors/paul_headshotx24.jpeg' == ht
