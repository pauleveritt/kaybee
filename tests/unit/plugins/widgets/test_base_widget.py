import pytest
from sphinx.application import Sphinx

from kaybee.plugins.widgets.base_widget import BaseWidget


@pytest.fixture()
def dummy_widget():
    yaml_content = """
name: this_id
template: dummy_listing
    """
    yield BaseWidget('somepage', 'listing', yaml_content)


class TestBaseWidget:
    def test_import(self):
        assert 'BaseWidget' == BaseWidget.__name__

    def test_instance(self, dummy_widget: BaseWidget):
        assert 'somepage' == dummy_widget.docname
        assert 'listing' == dummy_widget.wtype
        assert 'this_id' == dummy_widget.props.name
        assert 'dummy_listing' == dummy_widget.props.template

    def test_repr(self, dummy_widget: BaseWidget):
        # The repr is primarily useful in pytest listing
        assert 'somepage-this_id' == repr(dummy_widget)

    def test_render(self, mocker,
                    sphinx_app: Sphinx, dummy_widget: BaseWidget):
        mocker.patch.object(sphinx_app.builder.templates, 'render',
                            return_value='<p>Hello 9293</p>')
        sphinx_app.resources = {dummy_widget.docname: dict(flag=912)}
        context = dict(previous=1)
        result = dummy_widget.render(sphinx_app, context)
        assert 'somepage' == dummy_widget.docname
        assert '<p>Hello 9293</p>' == result

    def test_to_json(self, dummy_widget: BaseWidget):
        actual = dummy_widget.__json__()
        assert 'somepage' == actual['docname']
        assert 'dummy_listing' == actual['template']
        assert 'listing' == actual['wtype']
        assert {'name': 'this_id',
                'template': 'dummy_listing'} == actual['props']
        assert 'somepage-this_id' == actual['repr']
