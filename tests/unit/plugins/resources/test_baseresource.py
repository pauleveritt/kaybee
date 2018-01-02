import pytest

from kaybee.plugins.resources.base_resource import (
    parse_parent,
    BaseResource,
)


class TestBaseResourceParseParent:
    def test_import(self):
        assert 'parse_parent' == parse_parent.__name__

    @pytest.mark.parametrize('docname, parent', [
        ('index', None),
        ('about', 'index'),
        ('blog/index', 'index'),
        ('blog/about', 'blog/index'),
        ('blog/s1/index', 'blog/index'),
        ('blog/s1/about', 'blog/s1/index'),
        ('blog/s1/s2/index', 'blog/s1/index'),
        ('blog/s1/s2/about', 'blog/s1/s2/index'),
        ('blog/s1/s2/s3/index', 'blog/s1/s2/index'),
        ('blog/s1/s2/s3/about', 'blog/s1/s2/s3/index'),
    ])
    def test_parse_parent(self, docname, parent):
        this_parent = parse_parent(docname)
        assert parent == this_parent


class TestBaseResource:
    def test_import(self):
        assert 'BaseResource' == BaseResource.__name__

    def test_instance(self):
        br = BaseResource('somepage', 'resource', '')
        assert 'somepage' == br.docname
        assert 'resource' == br.rtype
        assert 'index' == br.parent
        assert 1 == br.props.auto_excerpt

    def test_repr(self):
        # The repr is primarily useful in pytest listing
        br = BaseResource('somepage', 'resource', '')
        assert 'somepage' == repr(br)

    @pytest.mark.parametrize('docname, parents_len, parentname', [
        ('index', 0, 'site'),
        ('about', 1, 'index'),
        ('r1/index', 1, 'index'),
        ('r1/about', 2, 'r1/index'),
        ('r1/r2/index', 2, 'r1/index'),
        ('r1/r2/about', 3, 'r1/r2/index'),
        ('r1/r2/r3/index', 3, 'r1/r2/index'),
        ('r1/r2/r3/about', 4, 'r1/r2/r3/index'),
    ])
    def test_root_parents(self, sample_resources, docname, parents_len,
                          parentname):
        a = sample_resources[docname]
        parents = a.parents(sample_resources)
        assert parents_len == len(parents)
        if parents_len:
            assert 'index' == parents[-1].docname  # Homepage
            assert parentname == parents[0].docname

    def test_to_json(self, sample_resources):
        r4about = 'r1/r2/r3/r4/about'
        actual = sample_resources[r4about].__json__(sample_resources)
        assert 'r1/r2/r3/r4/about' == actual['docname']
        assert 'resource' == actual['rtype']
        assert 'r1/r2/r3/r4/index' == actual['parent']
        assert 1 == actual['props']['auto_excerpt']