import inspect
import os
from typing import List, Dict

from docutils.readers import doctree
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.jinja2glue import SphinxFileSystemLoader

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.resources.action import ResourceAction
from kaybee.plugins.resources.container import ResourcesContainer
from kaybee.plugins.resources.directive import ResourceDirective


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


@kb.event(SphinxEvent.EBRD, scope='resource', system_order=55)
def add_directives(kb_app: kb,
                   sphinx_app: Sphinx,
                   sphinx_env: BuildEnvironment,
                   docnames=List[str],
                   ):
    """ For each resource type, register a new Sphinx directive """

    for k, v in list(kb_app.config.resources.items()):
        sphinx_app.add_directive(k, ResourceDirective)


@kb.event(SphinxEvent.HPC, scope='resource')
def resource_into_html_context(
        kb_app: kb,
        sphinx_app: Sphinx,
        pagename,
        templatename: str,
        context,
        doctree: doctree) -> Dict[str, str]:

    # Get the resource for this pagename. If no match, then this pagename
    # must be a genericpage
    resources = sphinx_app.resources
    resource = resources.get(pagename)
    if resource:
        context['resource'] = resource
        templatename = resource.template(resources) + '.html'
        return dict(templatename=templatename)


@kb.dumper('resources')
def dump_settings(kb_app: kb, sphinx_env: BuildEnvironment):
    # First get the kb app configuration for resources
    config = {
        k: v.__module__ + '.' + v.__name__
        for (k, v) in kb_app.config.resources.items()
    }

    # Next, get the actual resources in the app.resources DB
    resources = sphinx_env.app.resources
    values = {k: v.__json__(resources) for (k, v) in resources.items()}
    resources = dict(
        config=config,
        values=values
    )
    return dict(resources=resources)
