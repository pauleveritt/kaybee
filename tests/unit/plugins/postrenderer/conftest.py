import datetime

import dectate
import pytest

from kaybee.plugins.debugdumper.action import DumperAction
from kaybee.plugins.resources.action import ResourceAction


@pytest.fixture()
def debugdumper_kb_app():
    class debugdumper_kb_app(dectate.App):
        resource = dectate.directive(ResourceAction)
        dumper = dectate.directive(DumperAction)

    yield debugdumper_kb_app


@pytest.fixture()
def conflicting_events(debugdumper_kb_app):
    # Omit the "order" to disambiguate
    @debugdumper_kb_app.dumper('resources')
    def dumpresources1(*args):
        return

    @debugdumper_kb_app.dumper('resources')
    def dumpresources2(*args):
        return

    yield (dumpresources1, dumpresources2)


@pytest.fixture()
def register_valid_event(debugdumper_kb_app):
    @debugdumper_kb_app.dumper('resources')
    def handle_event(debugdumper_kb_app=None, sphinx_env=None):
        return dict(
            resource=dict(
                published=datetime.datetime.now()

            )
        )

    dectate.commit(debugdumper_kb_app)
    yield handle_event
