import inspect
import os
from typing import List

from docutils import nodes
from docutils.readers import doctree
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment
from sphinx.jinja2glue import SphinxFileSystemLoader

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.widgets.action import WidgetAction
from kaybee.plugins.widgets.node import widget
from kaybee.plugins.widgets.directive import WidgetDirective


@kb.event(SphinxEvent.BI, scope='widgets')
def add_widget_node(kb_app: kb, sphinx_app: Sphinx):
    sphinx_app.add_node(widget)


@kb.event(SphinxEvent.EBRD, scope='widgets', system_order=40)
def initialize_widgets_container(kb_app: kb,
                                 sphinx_app: Sphinx,
                                 sphinx_env: BuildEnvironment,
                                 docnames=List[str],
                                 ):
    if not hasattr(sphinx_app.env, 'widgets'):
        sphinx_app.env.widgets = dict()


@kb.event(SphinxEvent.EBRD, scope='widgets', system_order=50)
def register_template_directory(kb_app: kb,
                                sphinx_app: Sphinx,
                                sphinx_env: BuildEnvironment,
                                docnames=List[str],
                                ):
    """ Add this widget's templates dir to template paths """

    template_bridge = sphinx_app.builder.templates

    actions = WidgetAction.get_callbacks(kb_app)

    for action in actions:
        f = os.path.dirname(inspect.getfile(action))
        template_bridge.loaders.append(SphinxFileSystemLoader(f))


@kb.event(SphinxEvent.EBRD, scope='widgets', system_order=60)
def register_widget_directive(kb_app: kb,
                              sphinx_app: Sphinx,
                              sphinx_env: BuildEnvironment,
                              docnames=List[str],
                              ):
    # Register a directive
    for k, v in list(kb_app.config.widgets.items()):
        sphinx_app.add_directive(k, WidgetDirective)


@kb.event(SphinxEvent.DRES, scope='widgets')
def render_widgets(kb_app: kb,
                   sphinx_app: Sphinx,
                   doctree: doctree,
                   fromdocname: str,
                   ):
    """ Go through docs and replace widget directive with rendering """

    builder: StandaloneHTMLBuilder = sphinx_app.builder

    for node in doctree.traverse(widget):
        # Render the output
        w = sphinx_app.env.widgets.get(node.name)
        context = builder.globalcontext.copy()

        # Add in certain globals
        context['resources'] = sphinx_app.env.resources
        context['references'] = sphinx_app.env.references
        output = w.render(sphinx_app, context)

        # Put the output into the node contents
        listing = [nodes.raw('', output, format='html')]
        node.replace_self(listing)


@kb.dumper('widgets')
def dump_settings(kb_app: kb, sphinx_env: BuildEnvironment):
    # First get the kb app configuration for widgets
    config = {
        k: v.__module__ + '.' + v.__name__
        for (k, v) in kb_app.config.widgets.items()
    }

    # Next, get the actual widgets in the app.widgets DB
    widgets = sphinx_env.widgets
    values = {k: v.__json__() for (k, v) in widgets.items()}

    widgets = dict(
        config=config,
        values=values
    )
    return dict(widgets=widgets)
