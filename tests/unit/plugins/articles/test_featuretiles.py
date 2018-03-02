import pytest

from kaybee.plugins.articles.featuretiles import FeaturetilesWidget


@pytest.fixture()
def dummy_featuretiles():
    yaml = """
name: vp1
    """
    vp = FeaturetilesWidget('widget1', 'widget1', yaml)
    yield vp


class TestFeaturetiles:
    def test_import(self):
        assert 'FeaturetilesWidget' == FeaturetilesWidget.__name__

    def test_construction(self, dummy_featuretiles: FeaturetilesWidget):
        assert 'vp1' == dummy_featuretiles.props.name
