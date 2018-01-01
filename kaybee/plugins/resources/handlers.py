import inspect
from typing import List

import os
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.jinja2glue import SphinxFileSystemLoader

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.resources.action import ResourceAction
from kaybee.plugins.resources.container import ResourcesContainer


@kb.event(SphinxEvent.BI, scope='resources')
def handle_builderinited(kb_app: kb, sphinx_app: Sphinx):
    pass


@kb.event(SphinxEvent.EBRD, scope='resource', system_order=40)
def initialize_resources_container(kb_app: kb,
                                   sphinx_app: Sphinx,
                                   sphinx_env: BuildEnvironment,
                                   docnames=List[str],
                                   ):
    sphinx_app.resources = ResourcesContainer()


@kb.event(SphinxEvent.EBRD, scope='resource', system_order=50)
def register_template_directory(kb_app: kb,
                                sphinx_app: Sphinx,
                                sphinx_env: BuildEnvironment,
                                docnames=List[str],
                                ):
    """ Add this resource's templates dir to template paths """

    template_bridge = sphinx_app.builder.templates

    actions = ResourceAction.get_callbacks(kb_app)

    for action in actions:
        f = os.path.dirname(inspect.getfile(action))
        template_bridge.loaders.append(SphinxFileSystemLoader(f))


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
