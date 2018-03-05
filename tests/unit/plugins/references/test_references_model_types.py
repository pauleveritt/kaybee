import pytest

from kaybee.plugins.resources.resource import BaseResource


@pytest.fixture()
def good_resource():
    yaml = """
references:
    reference: [a, b, c]
    """

    yield BaseResource('doc1', 'resource', yaml)


class TestReferencesType:
    def test_good_resources(self, good_resource: BaseResource):
        assert 'doc1' == good_resource.docname
        refs = good_resource.props.references
        r = refs['reference']
        assert ['a', 'b', 'c'] == r
