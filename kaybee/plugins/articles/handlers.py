"""

TODO
- excerpt and auto-excerpt (and remove other)
-
"""

import inspect
import os
from typing import List

from docutils import nodes
from docutils.readers import doctree
from sphinx.addnodes import toctree
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment
from sphinx.jinja2glue import SphinxFileSystemLoader

from kaybee.app import kb
from kaybee.plugins.articles.actions import ToctreeAction
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.settings.model import KaybeeSettings


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
        custom_toctree = registered_toctree()
        context = builder.globalcontext.copy()
        context['sphinx_app'] = sphinx_app

        # The challenge here is that some items in a toctree
        # might not be resources in our "database". So we have
        # to ask Sphinx to get us the titles.
        custom_toctree.set_entries(node.attributes['entries'], env.titles,
                                   sphinx_app.resources)
        output = custom_toctree.render(builder, context, sphinx_app)

        # Put the output into the node contents
        listing = [nodes.raw('', output, format='html')]
        node.replace_self(listing)


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

#
# ## Resource 'doctree-read' event, gets just the data into the resource state
#         # Step 3: Find any toctrees (at most one, hopefully) and record
#         for node in doctree.traverse(toctree):
#             resource.toctree = [
#                 target for (flag, target) in node.attributes['entries']
#             ]
#             pass
