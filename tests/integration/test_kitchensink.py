"""

TODO
- Custom: resource, widget, reference, genericpage, localtemplates
- Custom: article, article_reference, homepage, section, toctree

"""

import pytest

pytestmark = pytest.mark.sphinx('html', testroot='kitchensink')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
def test_homepage(page):
    h1 = page.find('h1').contents[0].strip()
    assert 'Kitchen Sink' == h1

    kb_body = page.find(id='kb-body')
    nav = kb_body.find_all(class_='kb-navmenu-item')

    # kb-body stuff
    assert 'homepage' == kb_body.find(id='kb-rtype').contents[0].strip()
    assert 'index' == kb_body.find(id='kb-docname').contents[0].strip()
    assert 'Kitchen Sink' == kb_body.find(id='kb-title').contents[0].strip()

    # Nav menu
    navitems = [navitem.contents[0].strip() for navitem in nav]
    assert 'Contact Us' in navitems
    assert 'About Us' in navitems
    assert 'Intro to Django' in navitems
    assert 'Hidden' not in navitems

    # Toctree
    toctree = page.find_all(class_='kb-toctree')
    assert 1 == len(toctree)
    anchors = [
        (a.attrs['href'], a.contents[0].strip())
        for a in toctree[0].find_all(class_='reference internal')
    ]
    assert 2 == len(anchors)
    assert 'hidden.html' in anchors[0][0]
    assert 'Hidden' == anchors[0][1]
    assert 'categories/index.html' in anchors[1][0]
    assert 'Category Listing' == anchors[1][1]


@pytest.mark.parametrize('page', ['2018/intro_django.html', ], indirect=True)
def test_article(page):
    h1 = page.find('h1').contents[0].strip()
    assert 'Intro to Django' == h1

    # videoplayer
    vp = page.find(class_='kb-videoplayer')
    width = vp.attrs['width']
    assert '640' == width

    # Category listing
    categories = [i.contents[0].strip()
                  for i in page.find_all(class_='kb-category-item')]
    assert 'Django' in categories
    assert 'Database' in categories

    # kb-body stuff
    kb_body = page.find(id='kb-body')
    assert 'article' == kb_body.find(id='kb-rtype').contents[0].strip()
    assert '2018/intro_django' == kb_body.find(id='kb-docname').contents[
        0].strip()
    assert 'Intro to Django' == kb_body.find(id='kb-title').contents[0].strip()


@pytest.mark.parametrize('page', ['categories/django.html', ], indirect=True)
def test_category(page):
    h1 = page.find('h1').contents[0].strip()
    assert 'Django' == h1

    # Target references listing
    references = [i.contents[0].strip()
                  for i in page.find_all(class_='kb-reference-item')]
    assert 'Intro to Django' in references

    # kb-body stuff
    kb_body = page.find(id='kb-body')
    assert 'category' == kb_body.find(id='kb-rtype').contents[0].strip()
    assert 'categories/django' == kb_body.find(id='kb-docname').contents[
        0].strip()
    assert 'Django' == kb_body.find(id='kb-title').contents[0].strip()


@pytest.mark.parametrize('page', ['2018/index.html', ], indirect=True)
def test_section(page):
    h1 = page.find('h1').contents[0].strip()
    assert '2018 Articles' == h1

    # Querylist widget
    labels = [i.contents[0].strip()
              for i in page.find_all(class_='kb-querylist-label')]
    assert 'Recent Sections' in labels
    assert 'Recent Articles' in labels

    results = [i.contents[0].strip()
               for i in page.find_all(class_='kb-querylist-item')]
    assert '2018 Articles' in results
    assert 'About Us' in results

    # kb-body stuff
    kb_body = page.find(id='kb-body')
    assert 'section' == kb_body.find(id='kb-rtype').contents[0].strip()
    assert '2018/index' == kb_body.find(id='kb-docname').contents[
        0].strip()
    assert '2018 Articles' == kb_body.find(id='kb-title').contents[0].strip()


@pytest.mark.parametrize('page', ['2018/ksresource1.html', ], indirect=True)
def test_ksresource(page):
    h1 = page.find('h1').contents[0].strip()
    assert 'KSResource 1' == h1

    flag = page.find(id='kb-ksresource-flag').contents[0].strip()
    assert '9' == flag
    increment = page.find(id='kb-ksresource-increment').contents[0].strip()
    assert '10' == increment

    # kb-body stuff
    kb_body = page.find(id='kb-body')
    assert 'ksresource' == kb_body.find(id='kb-rtype').contents[0].strip()
    assert '2018/ksresource1' == kb_body.find(id='kb-docname').contents[
        0].strip()
    assert 'KSResource 1' == kb_body.find(id='kb-title').contents[0].strip()


@pytest.mark.parametrize('page', ['2018/ksresource1.html', ], indirect=True)
def test_kswidget(page):
    h1 = page.find('h1').contents[0].strip()
    assert 'KSResource 1' == h1

    flag = page.find(id='kb-kswidget-flag').contents[0].strip()
    assert '9' == flag
    increment = page.find(id='kb-kswidget-increment').contents[0].strip()
    assert '10' == increment
    another_flag = page.find(id='kb-kswidget-anotherflag').contents[0].strip()
    assert '835' == another_flag


@pytest.mark.parametrize('page', ['2018/ksarticle1.html', ], indirect=True)
def test_ksarticle(page):
    h1 = page.find('h1').contents[0].strip()
    assert 'KSArticle 1' == h1

    flag = page.find(id='kb-ksarticle-flag').contents[0].strip()
    assert '9' == flag
    increment = page.find(id='kb-ksarticle-increment').contents[0].strip()
    assert '10' == increment

    # kb-body stuff
    kb_body = page.find(id='kb-body')
    assert 'ksarticle' == kb_body.find(id='kb-rtype').contents[0].strip()
    assert '2018/ksarticle1' == kb_body.find(id='kb-docname').contents[
        0].strip()
    assert 'KSArticle 1' == kb_body.find(id='kb-title').contents[0].strip()


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestResourceDebug:

    def test_settings(self, json_page):
        assert 'use_debug' in json_page['settings']['debugdumper']
