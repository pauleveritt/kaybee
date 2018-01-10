import pytest
from sphinx.application import Sphinx

from kaybee.plugins.widgets.base_widget import BaseWidget


@pytest.fixture()
def listing_widget():
    class ListingWidget(BaseWidget):
        def make_context(self, context, sphinx_app):
            return dict(class_flag=912)
            
    yaml_content = """
name: this_id
template: dummy_listing
    """
    yield ListingWidget('somepage', 'listing', yaml_content)


class TestBaseWidget:
    def test_import(self):
        assert 'BaseWidget' == BaseWidget.__name__

    def test_instance(self, listing_widget: BaseWidget):
        assert 'somepage' == listing_widget.docname
        assert 'listing' == listing_widget.wtype
        assert 'this_id' == listing_widget.props.name
        assert 'dummy_listing' == listing_widget.props.template

    def test_broken_instance(self, listing_widget: BaseWidget):
        # Class doesn't implement make_context
        assert 'somepage' == listing_widget.docname
        assert 'listing' == listing_widget.wtype
        assert 'this_id' == listing_widget.props.name
        assert 'dummy_listing' == listing_widget.props.template

    def test_repr(self, listing_widget: BaseWidget):
        # The repr is primarily useful in pytest listing
        assert 'somepage-this_id' == repr(listing_widget)

    def test_missing_make_context(self):
        yaml_content = """
        name: this_id
        template: dummy_listing
            """
        bw = BaseWidget('somepage', 'listing', yaml_content)
        with pytest.raises(NotImplementedError):
            bw.make_context(dict(), dict())

    def test_render(self, mocker,
                    sphinx_app: Sphinx, listing_widget: BaseWidget):
        mocker.patch.object(sphinx_app.builder.templates, 'render',
                            return_value='<p>Hello 9293</p>')
        sphinx_app.resources = {listing_widget.docname: dict(flag=912)}
        context = dict(previous=1)
        result = listing_widget.render(sphinx_app, context)
        assert 'somepage' == listing_widget.docname
        assert '<p>Hello 9293</p>' == result

    def test_to_json(self, listing_widget: BaseWidget):
        actual = listing_widget.__json__()
        assert 'somepage' == actual['docname']
        assert 'dummy_listing' == actual['template']
        assert 'listing' == actual['wtype']
        assert {'name': 'this_id',
                'template': 'dummy_listing'} == actual['props']
        assert 'somepage-this_id' == actual['repr']
