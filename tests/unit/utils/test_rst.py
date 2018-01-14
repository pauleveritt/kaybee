from kaybee.utils.rst import (
    rst_to_html,
    get_rst_excerpt,
    get_rst_title,
    rst_document,
)


class TestRstDocument:
    def test_import(self):
        assert 'rst_document' == rst_document.__name__

    def test_rst_document(self):
        source = 'Hello *world*'
        result = rst_document(source)
        assert 'document' == result.__class__.__name__


class TestRstToHtml:
    def test_import(self):
        assert 'rst_to_html' == rst_to_html.__name__

    def test_rst_to_html(self):
        source = 'Hello *world*'
        result = rst_to_html(source)
        assert '<div class="document">' in result
        assert '<p>Hello <em>world</em></p>' in result
        assert '</div>' in result


class TestRstTitle:
    def test_import(self):
        assert 'get_rst_title' == get_rst_title.__name__

    def test_with_title(self, title_doc):
        result = get_rst_title(title_doc)
        assert 'Test Simple' == result

    def test_without_title(self, notitle_doc):
        result = get_rst_title(notitle_doc)
        assert None is result


class TestGetRstExcerpt:
    def test_import(self):
        assert 'get_rst_excerpt' == get_rst_excerpt.__name__

    def test_default(self, excerpt):
        """ By default, use the first paragraph """
        result = get_rst_excerpt(excerpt)
        assert 'First paragraph.' == result

    def test_noparagraphs(self, noexcerpt):
        """ Document has no paragraphs """
        result = get_rst_excerpt(noexcerpt)
        assert '' == result

    def test_multiple_paragraphs(self, excerpt):
        """ By configuration, you can ask for more paragraphs """

        result = get_rst_excerpt(excerpt, 2)
        assert 'First paragraph. Second paragraph.' == result
