import pytest

from kaybee.plugins.articles.videoplayer import VideoPlayer


@pytest.fixture()
def dummy_videoplayer():
    yaml = """
src: http://fool.com
width: 99
    """
    vp = VideoPlayer('widget1', 'widget1', yaml)
    yield vp


class TestVideoPlayer:
    def test_import(self):
        assert 'VideoPlayer' == VideoPlayer.__name__

    def test_construction(self, dummy_videoplayer: VideoPlayer):
        assert 99 == dummy_videoplayer.props.width

    def test_make_context(self, dummy_videoplayer: VideoPlayer):
        result = dummy_videoplayer.make_context(dict(), dict())
        assert None is result
