import pytest

from kaybee.plugins.widgets.base_widget import (
    BaseWidget,
    BaseWidgetModel,
)
from kaybee.plugins.widgets.node import widget


class DummyWidgetModel(BaseWidgetModel):
    flag: int = None


class DummyWidget(BaseWidget):
    model = DummyWidgetModel


@pytest.fixture()
def base_widget():
    content = """
name: widget1
template: widget1.html
kbtype: section
    """
    yield DummyWidget('somewidget', 'dummywidget', content)


class TestWidgetNode:

    def test_import(self):
        assert widget.__name__ == 'widget'

    def test_construction(self, base_widget):
        assert base_widget.__class__.__name__ == 'DummyWidget'
