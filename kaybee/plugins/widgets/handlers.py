from docutils import nodes
from docutils.readers import doctree
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.widgets.node import widget


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
        w = sphinx_app.widgets.get(node.name)
        context = builder.globalcontext.copy()
        output = w.render(builder.templates, context)

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

    widgets = dict(
        config=config,
    )
    return dict(widgets=widgets)
