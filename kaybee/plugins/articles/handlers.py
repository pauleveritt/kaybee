import inspect
import os
from operator import attrgetter
from pathlib import PurePath
from typing import List, Dict

from docutils import nodes
from docutils.readers import doctree
from sphinx.addnodes import toctree
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment
from sphinx.jinja2glue import SphinxFileSystemLoader

from kaybee.app import kb
from kaybee.plugins.articles.actions import ToctreeAction
from kaybee.plugins.articles.filters import DatetimeFilter
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.settings.model import KaybeeSettings
from kaybee.utils.rst import get_rst_excerpt


@kb.event(SphinxEvent.BI, scope='articles')
def register_filters(kb_app: kb, sphinx_app: Sphinx):
    dtf = DatetimeFilter(sphinx_app)
    filters = sphinx_app.builder.templates.environment.filters
    filters['datetime_fmt'] = dtf


@kb.event(SphinxEvent.EBRD, scope='toctrees')
def register_template_directory(kb_app: kb,
                                sphinx_app: Sphinx,
                                sphinx_env: BuildEnvironment,
                                docnames=List[str],
                                ):
    """ Add this widget's templates dir to template paths """

    template_bridge = sphinx_app.builder.templates

    actions = ToctreeAction.get_callbacks(kb_app)

    for action in actions:
        f = os.path.dirname(inspect.getfile(action))
        template_bridge.loaders.append(SphinxFileSystemLoader(f))


@kb.event(SphinxEvent.DRES, scope='toctrees')
def render_toctrees(kb_app: kb, sphinx_app: Sphinx, doctree: doctree,
                    fromdocname: str):
    """ Look in doctrees for toctree and replace with custom render """

    # Only do any of this if toctree support is turned on in KaybeeSettings.
    # By default, this is off.
    settings: KaybeeSettings = sphinx_app.config.kaybee_settings
    if not settings.articles.use_toctree:
        return

    # Setup a template and context
    builder: StandaloneHTMLBuilder = sphinx_app.builder
    env: BuildEnvironment = sphinx_app.env

    # Toctree support. First, get the registered toctree class, if any
    registered_toctree = ToctreeAction.get_for_context(kb_app)
    for node in doctree.traverse(toctree):
        if node.attributes['hidden']:
            continue
        custom_toctree = registered_toctree(fromdocname)
        context = builder.globalcontext.copy()
        context['sphinx_app'] = sphinx_app

        # Get the toctree entries. We only handle one level of depth for
        # now. To go further, we need to recurse like sphinx's
        # adapters.toctree._toctree_add_classes function
        entries = node.attributes['entries']

        # The challenge here is that some items in a toctree
        # might not be resources in our "database". So we have
        # to ask Sphinx to get us the titles.
        custom_toctree.set_entries(entries, env.titles,
                                   sphinx_app.env.resources)
        output = custom_toctree.render(builder, context, sphinx_app)

        # Put the output into the node contents
        listing = [nodes.raw('', output, format='html')]
        node.replace_self(listing)


@kb.event(SphinxEvent.DREAD, scope='toctrees')
def resource_toctrees(kb_app: kb,
                      sphinx_app: Sphinx,
                      doctree: doctree):
    # Find any toctrees in doc (at most one, hopefully) and record
    # onto the resource state

    # First, find out which resource this is. Won't be easy.
    resources = sphinx_app.env.resources
    confdir = sphinx_app.confdir
    source = PurePath(doctree.attributes['source'])

    # Get the relative path inside the docs dir, without .rst, then
    # get the resource
    docname = str(source.relative_to(confdir)).split('.rst')[0]
    resource = resources.get(docname)

    if resource:
        for node in doctree.traverse(toctree):
            resource.toctree = [
                target for (flag, target) in node.attributes['entries']
            ]
            pass


@kb.event(SphinxEvent.DREAD, scope='articles')
def stamp_excerpt(kb_app: kb,
                  sphinx_app: Sphinx,
                  doctree: doctree):
    """ Walk the tree and extract excert into resource.excerpt """

    # First, find out which resource this is. Won't be easy.
    resources = sphinx_app.env.resources
    confdir = sphinx_app.confdir
    source = PurePath(doctree.attributes['source'])

    # Get the relative path inside the docs dir, without .rst, then
    # get the resource
    docname = str(source.relative_to(confdir)).split('.rst')[0]
    resource = resources.get(docname)

    if resource:
        # Stamp the excerpt on the resource
        excerpt = getattr(resource.props, 'excerpt', False)
        auto_excerpt = getattr(resource.props, 'auto_excerpt', False)
        if excerpt:
            resource.excerpt = excerpt
        elif not auto_excerpt:
            resource.excerpt = None
        else:
            # Extract the excerpt based on the number of paragraphs
            # in auto_excerpt
            resource.excerpt = get_rst_excerpt(doctree, auto_excerpt)


@kb.event(SphinxEvent.HPC, scope='articles')
def articles_into_html_context(
        kb_app: kb,
        sphinx_app: Sphinx,
        pagename,
        templatename: str,
        context,
        doctree: doctree) -> Dict[str, str]:
    resources = sphinx_app.env.resources
    navitems = [
        resource
        for resource in resources.values()
        if getattr(resource.props, 'in_nav', False)
    ]
    context['navmenu'] = sorted(navitems,
                                key=lambda x: (
                                    x.props.weight, attrgetter('title')(x))
                                )


@kb.dumper('toctrees')
def dump_settings(kb_app: kb, sphinx_env: BuildEnvironment):
    # First get the kb app configuration for widgets
    config = {
        k: v.__module__ + '.' + v.__name__
        for (k, v) in kb_app.config.toctrees.items()
    }

    toctrees = dict(
        config=config,
    )
    return dict(toctrees=toctrees)
