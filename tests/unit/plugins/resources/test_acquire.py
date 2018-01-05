import pytest

from kaybee.plugins.resources.resource import Resource


class Article(Resource):
    pass


class Homepage(Resource):
    pass


class Section(Resource):
    pass


@pytest.fixture()
def resources():
    f1_content = """
    template: f1_section_template
    acquireds:
        article:
            template: acquired_article
        section:
            template: f1template
        all:
            flag: 9933
        """
    f4_content = """
    acquireds:
        all:
    """
    index = Homepage('index', 'homepage', '')
    about = Article('about', 'article', '')
    f1 = Section('f1/index', 'section', f1_content)
    f1_about = Article('f1/about', 'article', '')
    f2 = Section('f1/f2/index', 'section', '')
    f2.title = 'F2 Index'
    f2_about = Article('f1/f2/about', 'article', '')
    f2_about.title = 'F2 About'
    f3 = Section('f1/f2/f3/index', 'section', 'template: f3template')
    f3_about = Article('f1/f2/f3/about', 'article', '')
    f4 = Section('f1/f2/f3/f4/index', 'section', f4_content)
    f4_about = Article('f1/f2/f3/f4/about', 'article', '')

    return {
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
def da(resources):
    yield resources['f1/f2/f3/about']


class TestResourcesFindProp:
    def test_import(self):
        assert 'Resource' == Resource.__name__

    def test_template_from_props(self, resources, da):
        expected = 'f1_section_template'
        assert expected == resources['f1/index'].template(resources)

    def test_article_template_from_props(self, resources, da):
        da = resources['f1/f2/index']
        actual = da.acquire(resources, 'template')
        assert 'f1template' == actual

    def test_section_template_from_props(self, resources):
        da = resources['f1/f2/f3/index']
        actual = da.acquire(resources, 'template')
        assert 'f3template' == actual

    def test_template_from_section(self, resources, da):
        expected = 'acquired_article'
        assert expected == da.template(resources)

    def test_template_from_class(self, resources, da):
        # Delete the lineage-inheried article template prop on the section
        f1 = resources['f1/index']
        del f1.props.acquireds['article']
        assert 'article' == da.template(resources)

    def test_template_from_resource(self, resources, da):
        # Test that 'resource' breaks the rules and returns 'page.html'
        r = Resource('f1/someresource', 'resource', '')
        resources['f1/someresource'] = r
        assert 'page' == r.template(resources)

    def test_flag_from_all_acquireds(self, resources):
        # Get a flag from the "all" section of acquireds
        da = resources['f1/f2/f3/index']
        assert '9933' == da.acquire(resources, 'flag')

    def test_empty_all_acquireds(self, resources):
        # Get a flag from the "all" section of acquireds
        da = resources['f1/f2/f3/f4/about']
        assert None is da.acquire(resources, 'bogus')
