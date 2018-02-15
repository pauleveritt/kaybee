import inspect
import os
from pathlib import PurePath
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
from kaybee.utils.rst import get_rst_title


@kb.event(SphinxEvent.BI, scope='resources')
def handle_builderinited(kb_app: kb, sphinx_app: Sphinx):
    pass


@kb.event(SphinxEvent.EBRD, scope='resource', system_order=40)
def initialize_resources_container(kb_app: kb,
                                   sphinx_app: Sphinx,
                                   sphinx_env: BuildEnvironment,
                                   docnames=List[str],
                                   ):
    if not hasattr(sphinx_app.env, 'resources'):
        sphinx_app.env.resources = ResourcesContainer()


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


@kb.event(SphinxEvent.EU, scope='resource')
def process_field_handlers(kb_app: kb,
                           sphinx_app: Sphinx,
                           sphinx_env: BuildEnvironment
                           ):
    resources = sphinx_app.env.resources
    for resource in resources.values():
        images = getattr(resource.props, 'images', None)
        if images:
            for prop in images:
                t = resource.props.fields['images'].type_
                if hasattr(prop, 'env_updated'):
                    prop.env_updated(
                        kb_app,
                        sphinx_app,
                        sphinx_env,
                        resource
                    )


@kb.event(SphinxEvent.DREAD, scope='resource')
def stamp_title(kb_app: kb,
                sphinx_app: Sphinx,
                doctree: doctree):
    """ Walk the tree and extra RST title into resource.title """

    # First, find out which resource this is. Won't be easy.
    resources = sphinx_app.env.resources
    confdir = sphinx_app.confdir
    source = PurePath(doctree.attributes['source'])

    # Get the relative path inside the docs dir, without .rst, then
    # get the resource
    docname = str(source.relative_to(confdir)).split('.rst')[0]
    resource = resources.get(docname)

    if resource:
        # Stamp the title on the resource
        title = get_rst_title(doctree)
        resource.title = title


@kb.event(SphinxEvent.HPC, scope='resource')
def resource_into_html_context(
        kb_app: kb,
        sphinx_app: Sphinx,
        pagename,
        templatename: str,
        context,
        doctree: doctree) -> Dict[str, str]:
    # Always put the resources db into Jinja2 context
    resources = sphinx_app.env.resources
    context['resources'] = resources

    # Get the resource for this pagename. If no match, then this pagename
    # must be a genericpage
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
    resources = sphinx_env.resources
    values = {k: v.__json__(resources) for (k, v) in resources.items()}
    resources = dict(
        config=config,
        values=values
    )
    return dict(resources=resources)
