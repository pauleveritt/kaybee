from pydantic import BaseModel

from kaybee.app import kb

from kaybee.plugins.widgets.base_widget import BaseWidget


class VideoPlayerModel(BaseModel):
    width: int = 640
    height: int = 360
    src: str
    frameborder: int = 0
    allowfullscreen: bool = True


@kb.widget('videoplayer')
class VideoPlayer(BaseWidget):
    model = VideoPlayerModel
    template = 'videoplayer'

    def make_context(self, context, sphinx_app):
        pass
