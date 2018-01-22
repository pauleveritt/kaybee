import dectate
import pytest
from pydantic import BaseModel

from kaybee.plugins.layouts.action import LayoutAction
from kaybee.plugins.layouts.base_layout import BaseLayout


@pytest.fixture()
def layouts_kb_app(kb_app):
    class layouts_kb_app(kb_app):
        layout = dectate.directive(LayoutAction)

    yield layouts_kb_app


@pytest.fixture()
def conflicting_layouts(layouts_kb_app):
    @layouts_kb_app.layout('mylayout')
    class Layout1(BaseLayout):
        pass

    @layouts_kb_app.layout('mylayout')
    class Layout2(BaseLayout):
        pass

    yield (Layout1, Layout2)


@pytest.fixture()
def valid_layouts(layouts_kb_app):
    @layouts_kb_app.layout('mylayout1')
    class Layout1(BaseLayout):
        pass

    @layouts_kb_app.layout('mylayout2')
    class Layout2(BaseLayout):
        pass

    dectate.commit(layouts_kb_app)
    yield (Layout1, Layout2)


@pytest.fixture()
def my_layout():
    # Make an instance of a layout
    class MyLayoutModel(BaseModel):
        copyright: str

    class MyLayout(BaseLayout):
        model = MyLayoutModel

    yield MyLayout(copyright='312')
