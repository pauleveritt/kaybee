from kaybee.plugins.queries.props_model import (
    BaseQueryModel,
    CorePropFilterModel,
)


class TestPropsModel:
    def test_imports(self):
        assert 'BaseQueryModel' == BaseQueryModel.__name__
        assert 'CorePropFilterModel' == CorePropFilterModel.__name__

    def test_construction(self):
        bqm = BaseQueryModel()
        assert 'title' == bqm.sort_value
        cpfm = CorePropFilterModel(
            **dict(
                key='excerpt',
                value=9
            )
        )
        assert 'excerpt' == cpfm.key