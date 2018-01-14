import pytest

from kaybee.plugins.articles.base_article import BaseArticle
from kaybee.plugins.articles.base_homepage import BaseHomepage
from kaybee.plugins.articles.base_section import BaseSection
from kaybee.plugins.articles.base_toctree import BaseToctree


@pytest.fixture()
def article_resources():
    f1_content = """
    template: f1_section_template
    featured_resource: f1/f2/about
    acquireds:
        article:
            template: acquired_article
            style: acquired_style
        section:
            template: f1template
        all:
            flag: 9933
        """
    f4_content = """
    acquireds:
        all:
    """
    index = BaseHomepage('index', 'homepage', 'logo: somelogo.png')
    about = BaseArticle('about', 'article', '')
    f1 = BaseSection('f1/index', 'section', f1_content)
    f1_about = BaseArticle('f1/about', 'article',
                           'published: 2015-04-25 12:01')
    f2 = BaseSection('f1/f2/index', 'section', '')
    f2.title = 'F2 Index'
    f2_about = BaseArticle('f1/f2/about', 'article', '')
    f2_about.title = 'F2 About'
    f3 = BaseSection('f1/f2/f3/index', 'section', 'template: f3template')
    f3_about = BaseArticle('f1/f2/f3/about', 'article', '')
    f4 = BaseSection('f1/f2/f3/f4/index', 'section', f4_content)
    f4_about = BaseArticle('f1/f2/f3/f4/about', 'article', '')

    yield {
        'index': index,
        'about': about,
        'f1/index': f1,
        'f1/about': f1_about,
        'f1/f2/index': f2,
        'f1/f2/about': f2_about,
        'f1/f2/f3/index': f3,
        'f1/f2/f3/about': f3_about,
        'f1/f2/f3/f4/index': f4,
        'f1/f2/f3/f4/about': f4_about,
    }


@pytest.fixture()
def dummy_article(article_resources):
    yield article_resources['f1/f2/f3/about']


@pytest.fixture()
def dummy_section(article_resources):
    yield article_resources['f1/f2/f3/index']


@pytest.fixture()
def dummy_homepage(article_resources):
    yield article_resources['index']


@pytest.fixture()
def dummy_nodes(dummy_entries):
    class Node:
        def __init__(self):
            self.attributes = dict(
                hidden=False,
                entries=dummy_entries,
            )

        def replace_self(self, value):
            pass

    yield (Node(),)


@pytest.fixture()
def dummy_doctree(dummy_nodes):
    class Doctree:
        def __init__(self):
            self.dummy_nodes = dummy_nodes

        def traverse(self, *args):
            return self.dummy_nodes

    yield Doctree()


@pytest.fixture()
def dummy_toctree():
    yield BaseToctree()


@pytest.fixture()
def dummy_entries():
    r = [
        ('x', 'f1/about')
    ]

    yield r


@pytest.fixture()
def dummy_titles():
    class Title:
        def __init__(self, first_child):
            self.children = [first_child]

    yield {
        'about': Title('About'),
        'f1/about': Title('F1 About')
    }


@pytest.fixture()
def article_env(dummy_titles):
    class Env:
        def __init__(self):
            self.titles = dummy_titles

    yield Env()
