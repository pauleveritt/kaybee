import pytest
from sphinx.application import Sphinx

from kaybee.plugins.widgets.base_widget import BaseWidget
from kaybee.plugins.widgets.base_widget import BaseWidgetModel


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


@pytest.fixture()
def no_template_widget():
    class ListingWidget(BaseWidget):
        def make_context(self, context, sphinx_app):
            return dict(class_flag=912)

    yaml_content = """
name: this_id
    """
    yield ListingWidget('somepage', 'listing', yaml_content)


@pytest.fixture()
def props_widget():
    class PropsWidgetModel(BaseWidgetModel):
        propswidget_flag: int

    class PropsWidget(BaseWidget):
        props: PropsWidgetModel

    yaml_content = """
name: this_id
propswidget_flag: 98
    """
    yield PropsWidget('somepage', 'propswidget', yaml_content)


class TestBaseWidget:
    def test_import(self):
        assert 'BaseWidget' == BaseWidget.__name__

    def test_instance(self, listing_widget: BaseWidget):
        assert 'somepage' == listing_widget.docname
        assert 'listing' == listing_widget.wtype
        assert 'this_id' == listing_widget.props.name
        assert 'dummy_listing' == listing_widget.props.template
        assert 'dummy_listing' == listing_widget.template

    def test_no_template_instance(self, no_template_widget: BaseWidget):
        assert 'somepage' == no_template_widget.docname
        assert 'listing' == no_template_widget.wtype
        assert 'this_id' == no_template_widget.props.name
        assert None is no_template_widget.props.template
        assert 'listing' == no_template_widget.template

    def test_extra_props(self, props_widget: BaseWidget):
        assert 'somepage' == props_widget.docname
        assert 'this_id' == props_widget.props.name
        assert 98 == props_widget.props.propswidget_flag

    def test_repr(self, listing_widget: BaseWidget):
        # The repr is primarily useful in pytest listing
        assert 'somepage-this_id' == repr(listing_widget)

    @pytest.mark.parametrize('current_docname, target_docname, expected', [
        ('2018/index', '2018/about', 'about'),
        ('2018/about', '2018/contact', 'contact'),
        ('2018/01/01/about', '2018/01/01/contact', 'contact'),
        ('2018/01/01/about', '2001/12/12/about', '../../../2001/12/12/about'),
    ])
    def test_pathto(self, listing_widget: BaseWidget,
                    current_docname, target_docname, expected):
        listing_widget.docname = current_docname
        assert expected == listing_widget.pathto_docname(target_docname)

    def test_render(self, mocker,
                    sphinx_app: Sphinx, listing_widget: BaseWidget):
        mocker.patch.object(sphinx_app.builder.templates, 'render',
                            return_value='<p>Hello 9293</p>')
        sphinx_app.env.resources = {listing_widget.docname: dict(flag=912)}
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
