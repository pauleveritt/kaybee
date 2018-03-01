from kaybee.app import kb

from kaybee.plugins.widgets.base_widget import (
    BaseWidget,
    BaseWidgetModel,
)


class VideoPlayerModel(BaseWidgetModel):
    width: int = 640
    height: int = 360
    src: str
    frameborder: int = 0
    allowfullscreen: bool = True


@kb.widget('videoplayer')
class VideoPlayer(BaseWidget):
    props: VideoPlayerModel
