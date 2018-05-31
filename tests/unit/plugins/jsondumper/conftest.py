import datetime

import dectate
import pytest

from kaybee.plugins.jsondumper.action import JsondumperAction
from kaybee.plugins.resources.action import ResourceAction


@pytest.fixture()
def jsondumper_kb_app():
    class jsondumper_kb_app(dectate.App):
        resource = dectate.directive(ResourceAction)
        jsondumper = dectate.directive(JsondumperAction)

    yield jsondumper_kb_app


@pytest.fixture()
def conflicting_events(jsondumper_kb_app):
    # Omit the "order" to disambiguate
    @jsondumper_kb_app.jsondumper('resources')
    def dumpresources1(*args):
        return

    @jsondumper_kb_app.jsondumper('resources')
    def dumpresources2(*args):
        return

    yield (dumpresources1, dumpresources2)


@pytest.fixture()
def register_valid_event(jsondumper_kb_app):
    @jsondumper_kb_app.jsondumper('resources')
    def handle_event(jsondumper_kb_app=None, sphinx_env=None):
        return dict(
            filename='unittest_results.json',
            results=[
                dict(
                    docname='a/b/1',
                    published=datetime.datetime.now()
                )
            ]
        )

    dectate.commit(jsondumper_kb_app)
    yield handle_event
