from kaybee.plugins.references.reference import Category


class TestCategory:
    def test_import(self):
        assert 'Category' == Category.__name__

    def test_construction(self):
        c = Category('category1', 'category', 'label: category1')
        assert True is c.is_reference
        assert 'category1' == c.docname
        assert 'category1' == c.props.label
