from kaybee.plugins.references.reference import Reference


class Testreference:
    def test_import(self):
        assert 'Reference' == Reference.__name__

    def test_construction(self):
        r1 = Reference('reference1', 'reference', 'label: reference1')
        assert True is r1.is_reference
        assert 'reference1' == r1.docname
        assert 'reference1' == r1.props.label
