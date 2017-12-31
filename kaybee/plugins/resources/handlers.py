from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent


@kb.event(SphinxEvent.BI, scope='resources')
def handle_builderinited(kb_app: kb, sphinx_app: Sphinx):
    pass


@kb.dumper('resources')
def dump_settings(kb_app: kb, sphinx_env: BuildEnvironment):
    # First get the kb app configuration for resources
    config = dict()

    # Next, get the actual resources in the app.resources DB
    values = dict()
    resources = dict(
        config=config,
        values=values
    )
    return dict(resources=resources)
