"""

TODO
- excerpt and auto-excerpt (and remove other)
-
"""

import inspect
import os
from typing import List

from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.jinja2glue import SphinxFileSystemLoader

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.articles.actions import ToctreeAction


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

#
# @kb.event('env-before-read-docs', 'coretoctree')
# def register_templates(kb, app, env, docnames):
#     """ Called from event dispatch, add resource dir to templates """
#
#     template_bridge = app.builder.templates
#
#     for v in list(kb.config.cores.values()):
#         f = os.path.dirname(inspect.getfile(v))
#         template_bridge.loaders.append(SphinxFileSystemLoader(f))
#
#
# @kb.event('doctree-resolved', 'widgets')
# def process_widget_nodes(kb: kb, app: Sphinx, doctree, fromdocname):
#     """ Callback registered with Sphinx's doctree-resolved event """
#     # Setup a template and context
#
#     builder: StandaloneHTMLBuilder = app.builder
#     env: BuildEnvironment = app.env
#     site: Site = env.site
#
#     # Toctree support. First, get the registered toctree class, if any
#     registered_toctree = kb.config.cores.get('toctree')
#
#     if registered_toctree:
#         for node in doctree.traverse(toctree):
#             if node.attributes['hidden']:
#                 continue
#
#             w = registered_toctree()
#             context = builder.globalcontext.copy()
#             context['site'] = site
#
#             # The challenge here is that some items in a toctree
#             # might not be resources in our "database". So we have
#             # to ask Sphinx to get us the titles.
#             w.set_entries(node.attributes['entries'], env.titles,
#                           site.resources)
#             output = w.render(builder, context, site)
#
#             # Put the output into the node contents
#             listing = [nodes.raw('', output, format='html')]
#             node.replace_self(listing)
#
#
# ## Resource 'doctree-read' event
#         # Step 3: Find any toctrees (at most one, hopefully) and record
#         for node in doctree.traverse(toctree):
#             resource.toctree = [
#                 target for (flag, target) in node.attributes['entries']
#             ]
#             pass
