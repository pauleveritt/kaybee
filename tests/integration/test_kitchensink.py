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
    assert 'Contact' in navitems
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
    assert 4 == len(anchors)
    assert 'hidden.html' in anchors[0][0]
    assert 'Hidden' == anchors[0][1]
    assert 'categories/index.html' in anchors[1][0]
    assert 'Category Listing' == anchors[1][1]

    # Featuretiles
    featuretiles = page.find_all(class_='kbb-featuretiles-tile')
    assert 6 == len(featuretiles)
    assert 'First Feature' == featuretiles[0].contents[0].strip()


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
    assert 'PostgreSQL' in categories

    # Inline references
    refs = page.find_all("a", class_="internal")
    derived_title = refs[0].find('em').contents[0].strip()
    assert 'Django' == derived_title
    explicit_title = refs[1].find('em').contents[0].strip()
    assert 'Django 2.0' == explicit_title

    # kb-body stuff
    kb_body = page.find(id='kb-body')
    assert 'article' == kb_body.find(id='kb-rtype').contents[0].strip()
    assert '2018/intro_django' == kb_body.find(id='kb-docname').contents[
        0].strip()
    assert 'Intro to Django' == kb_body.find(id='kb-title').contents[0].strip()


@pytest.mark.parametrize('page', ['builtin_references/builtinref1.html', ],
                         indirect=True)
def test_builtinreference1(page):
    # Using the built-in reference type
    h1 = page.find('h1').contents[0].strip()
    assert 'Builtin Ref 1' == h1

    # kb-body stuff...doesn't exist, this is page.html
    kb_body = page.find(id='kb-body')
    assert None is kb_body


@pytest.mark.parametrize('page', ['builtin_references/builtinref2.html', ],
                         indirect=True)
def test_builtinreference2(page):
    # Using the built-in reference type
    h1 = page.find('h1').contents[0].strip()
    assert 'Builtin Ref 2' == h1

    label = page.find(id='kb-reference-label').contents[0].strip()
    assert 'builtinref2' == label

    # kb-body stuff
    kb_body = page.find(id='kb-body')
    assert 'reference' == kb_body.find(id='kb-rtype').contents[0].strip()
    assert 'builtin_references/builtinref2' == \
           kb_body.find(id='kb-docname').contents[
               0].strip()
    assert 'Builtin Ref 2' == kb_body.find(id='kb-title').contents[0].strip()


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


@pytest.mark.parametrize('page', ['customcategories/databases.html', ],
                         indirect=True)
def test_custom_category(page):
    h1 = page.find('h1').contents[0].strip()
    assert 'Databases' == h1

    # Target references listing
    references = [i.contents[0].strip()
                  for i in page.find_all(class_='kb-reference-item')]
    assert 'KSArticle 1' in references

    # kb-body stuff
    kb_body = page.find(id='kb-body')
    assert 'ksfeature' == kb_body.find(id='kb-rtype').contents[0].strip()
    assert 'customcategories/databases' == \
           kb_body.find(id='kb-docname').contents[
               0].strip()
    assert 'Databases' == kb_body.find(id='kb-title').contents[0].strip()

    # Test the Jinja2 filter for date handling
    dtf = page.find(id='kb-datetime_filter').contents[0].strip()
    assert 'Oct 01' == dtf


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


@pytest.mark.parametrize('page', ['2017/index.html', ], indirect=True)
def test_sectionquery(page):
    h1 = page.find('h1').contents[0].strip()
    assert '2017 Articles' == h1

    # Sectionquery widget
    results = [i.contents[0].strip()
               for i in page.find_all(class_='kb-sectionquery-item')]
    assert ['KSArticle 1', 'KSArticle 2'] == results

    # kb-body stuff
    kb_body = page.find(id='kb-body')
    assert 'section' == kb_body.find(id='kb-rtype').contents[0].strip()
    assert '2017/index' == kb_body.find(id='kb-docname').contents[
        0].strip()
    assert '2017 Articles' == kb_body.find(id='kb-title').contents[0].strip()


@pytest.mark.parametrize('page', ['builtin_references/index.html', ],
                         indirect=True)
def test_genericpage(page):
    # These are controlled from an acquireds setting on
    # index.rst
    h1 = page.find('h1').contents[0].strip()
    assert 'Builtin References' == h1

    assert 'builtin_references/index' == \
           page.find(id='kb-genericpage-docname').contents[0].strip()
    assert 'kitchensink_genericpage' == \
           page.find(id='kb-genericpage-template').contents[0].strip()


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
