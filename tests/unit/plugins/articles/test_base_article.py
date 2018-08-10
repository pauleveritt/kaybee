import pytest
from kaybee.plugins.articles.base_article import (
    BaseArticle,
    BaseArticleModel,
)


class TestBaseArticle:
    def test_import(self):
        assert 'BaseArticle' == BaseArticle.__name__
        assert 'BaseArticleModel' == BaseArticleModel.__name__

    def test_section_f1(self, article_resources):
        a = BaseArticle('f1/f2/f3/another', 'rtype', '')
        result = a.section(article_resources)
        assert 'f1/f2/index' == result.docname

    def test_article_style_from_props(self, article_resources, dummy_article):
        style = dummy_article.acquire(article_resources, 'style')
        assert 'acquired_style' == style

    @pytest.mark.parametrize('docname, nav_href, expected', [
        ('f1/index', 'f1/index', True),
        ('f1/index', 'f2/index', False),
        ('f2/index', 'f1/index', False),
        ('f1/about', 'f1/index', True),
        ('f1/about', 'f2/index', False),
        ('f1/f2/index', 'f1/index', True),
        ('f1/f2/about', 'f2/index', False),
    ])
    def test_in_navitem(self, article_resources, docname, nav_href, expected):
        a = BaseArticle(docname, 'article', '')
        assert a.in_navitem(article_resources, nav_href) == expected

    def test_not_in_navitem(self, article_resources):
        a = BaseArticle('f1/f2/about', 'article', '')
        nav_href = 'f1/f3/about'
        assert not a.in_navitem(article_resources, nav_href)

    @pytest.mark.parametrize('content, expected', [
        ('', False),
        ('published: 2020-12-01 01:23', False),
        ('published: 2012-03-24 11:47', True),
    ])
    def test_is_published(self, content, expected):
        article = BaseArticle('d1/a1', 'article', content)
        assert expected is article.is_published

    def test_to_json(self, article_resources):
        f3about = article_resources['f1/f2/f3/about']
        result = f3about.__json__(article_resources)
        assert 'f1/f2/f3/about' == result['docname']
        assert 'article' == result['rtype']
        assert 'f1/f2/f3/index' == result['parent']
        assert 1 == result['props']['auto_excerpt']
        assert 'excerpt' not in result  # Blank values filtered out
        assert 'f1/f2/index' == result['section']
        assert 'toctree' not in result
        assert 0 == len(result['series'])

    def test_index(self, article_resources):
        index = article_resources['index']
        result = index.__json__(article_resources)
        assert 'index' == result['docname']
        assert None is result['parent']
        assert 'toctree' not in result
        assert None is result['series']


class TestFindPropItem:
    def test_find_prop_item(self, dummy_image_article):
        first_image = dummy_image_article.props.images[0]
        f1 = dummy_image_article.find_prop_item('images', 'usage',
                                                first_image.usage)
        assert first_image.filename == f1.filename

    def test_not_find_prop_item(self, dummy_image_article):
        f1 = dummy_image_article.find_prop_item('images', 'usage', 'xxx')
        assert None is f1

    def test_no_images(self, article_resources):
        index = article_resources['index']
        f1 = index.find_prop_item('images', 'usage', 'headshot')
        assert None is f1

    def test_empty_images(self, article_resources):
        index = article_resources['index']
        index.props.images = []
        f1 = index.find_prop_item('images', 'usage', 'headshot')
        assert None is f1


class TestSeries:
    def test_method_exists(self, article_resources):
        resource = article_resources['f1/f2/about']
        assert 'series' == resource.series.__name__

    def test_no_series(self, article_resources):
        section = article_resources['f1/f2/index']
        assert False is getattr(section.props, 'is_series')

    def test_series_values(self, article_resources):
        # Assign a toctree
        article_resources['f1/f2/f3/index'].toctree = [
            'f1/f2/f3/index',
            'f1/f2/f3/about'
        ]
        resource = article_resources['f1/f2/f3/about']
        series = resource.series(article_resources)
        assert 'F3' == series[0]['title']
        assert 'F3 About' == series[1]['title']

    def test_parent_does_not_want_series(self, article_resources):
        # Assign a toctree
        article_resources['f1/f2/f3/index'].toctree = [
            'f1/f2/f3/index',
            'f1/f2/f3/about'
        ]
        parent: BaseArticle = article_resources['f1/f2/f3/index']
        parent.props.is_series = False
        resource = article_resources['f1/f2/f3/about']
        series = resource.series(article_resources)
        assert None is series

    def test_series_empty(self, article_resources):
        # Do NOT assign a toctree
        resource = article_resources['f1/f2/f3/about']
        series = resource.series(article_resources)
        assert [] == series

    def test_series_no_parent(self, article_resources):
        # The resource is the root, doesn't have a parent
        resource: BaseArticle = article_resources['index']
        series = resource.series(article_resources)
        assert None is series

    def test_nonresource_in_toctree(self, article_resources):
        # The resource is the root, doesn't have a parent
        resource: BaseArticle = article_resources['f1/f2/f3/about']
        parent: BaseArticle = article_resources['f1/f2/f3/index']
        parent.toctree = [
            'f1/f2/f3/index',
            'f1/f2/f3/about',
            'xyzpdq'
        ]
        series = resource.series(article_resources)
        expected = len(parent.toctree) - 1
        assert expected == len(series)


class TestBreadcrumbs:
    def test_method_exists(self, article_resources):
        resource = article_resources['f1/f2/about']
        assert 'breadcrumbs' == resource.breadcrumbs.__name__

    def test_entries(self, article_resources):
        resource = article_resources['f1/f2/about']
        bc = resource.breadcrumbs(article_resources)
        assert 'Home' == bc[0]['label']
        assert 'F1' == bc[1]['label']
        assert 'F2 Index' == bc[2]['label']
        assert 'F2 About' == bc[3]['label']
        assert True == bc[3]['is_active']
