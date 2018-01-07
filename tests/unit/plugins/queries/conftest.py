import pytest

from kaybee.plugins.resources.base_resource import BaseResource


class Article(BaseResource):
    pass


class Homepage(BaseResource):
    pass


class Section(BaseResource):
    pass


@pytest.fixture()
def query_resources():
    c0 = "excerpt: I am c0"
    c1 = """
excerpt: I am c1
auto_excerpt: 10
    """
    c2 = """
excerpt: I am c2
auto_excerpt: 20
    """
    c3 = """
excerpt: I am c3
auto_excerpt: 30
    """

    s1 = Section('8783', 'section', c0)
    s1.title = 'The First'
    s2 = Section('1343', 'section', c0)
    s2.title = 'Second should sort ahead of first'
    s3 = Section('4675', 'section', c3)
    s3.title = 'Z Last weights first'
    s4 = Section('9856', 'section', c2)
    s4.title = 'Q Not Last No Weight'
    a1 = Article('4444', 'article', c1)
    a1.title = 'About'
    a2 = Article('23', 'article', '')
    a2.title = 'Unpublished'

    results = dict()
    for i in (s1, s2, s3, s4, a1, a2,):
        results[i.docname] = i

    yield results
