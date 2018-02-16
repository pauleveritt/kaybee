import datetime

import dectate
import pytest

from kaybee.plugins.postrenderer.action import PostrendererAction
from kaybee.plugins.resources.action import ResourceAction


@pytest.fixture()
def postrenderer_kb_app():
    class postrenderer_kb_app(dectate.App):
        resource = dectate.directive(ResourceAction)
        postrenderer = dectate.directive(PostrendererAction)

    yield postrenderer_kb_app


@pytest.fixture()
def conflicting_events(postrenderer_kb_app):
    # Omit the "order" to disambiguate
    @postrenderer_kb_app.postrenderer('capitalize')
    def capitalize1(*args):
        return

    @postrenderer_kb_app.postrenderer('capitalize')
    def capitalize2(*args):
        return

    yield (capitalize1, capitalize2)


@pytest.fixture()
def register_valid_event(postrenderer_kb_app):
    @postrenderer_kb_app.postrenderer('capitalize')
    def capitalize1(template, context):
        return dict(
            resource=dict(
                published=datetime.datetime.now()

            )
        )

    dectate.commit(postrenderer_kb_app)
    yield capitalize1
