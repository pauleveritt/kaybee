from kaybee.app import kb
from kaybee.plugins.layouts.base_layout import (
    BaseLayout,
    BaseLayoutModel,
)


class MyLayout1Settings(BaseLayoutModel):
    copyright: str


@kb.layout('mylayout1')
class MyLayout1(BaseLayout):
    model = MyLayout1Settings
