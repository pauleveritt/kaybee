import inspect
import os
from typing import List, Dict

from docutils.readers import doctree
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.jinja2glue import SphinxFileSystemLoader

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.layouts.action import LayoutAction


@kb.event(SphinxEvent.EBRD, scope='layouts', system_order=40)
def initialize_layout(kb_app: kb,
                      sphinx_app: Sphinx,
                      sphinx_env: BuildEnvironment,
                      docnames=List[str],
                      ):
    layout_instance = sphinx_app.config.html_theme

    # Is this a Kaybee Layout, or just a regular Sphinx theme?
    if hasattr(layout_instance, 'settings'):
        layout_instance.sphinx_app = sphinx_app
        sphinx_app.layout = layout_instance


@kb.event(SphinxEvent.EBRD, scope='layouts', system_order=50)
def register_template_directory(kb_app: kb,
                                sphinx_app: Sphinx,
                                sphinx_env: BuildEnvironment,
                                docnames=List[str],
                                ):
    template_bridge = sphinx_app.builder.templates

    actions = LayoutAction.get_callbacks(kb_app)

    for action in actions:
        fa = inspect.getfile(action)
        f = os.path.dirname(fa)
        template_bridge.loaders.append(SphinxFileSystemLoader(f))


@kb.event(SphinxEvent.HPC, scope='layouts')
def layout_into_html_context(
        kb_app: kb,
        sphinx_app: Sphinx,
        pagename,
        templatename: str,
        context,
        doctree: doctree):
    if hasattr(sphinx_app, 'layout'):
        context['layout'] = sphinx_app.layout


@kb.dumper('layouts')
def dump_settings(kb_app: kb, sphinx_env: BuildEnvironment):
    # First get the kb app configuration for layouts
    config = {
        k: v.__module__ + '.' + v.__name__
        for (k, v) in kb_app.config.layouts.items()
    }

    layouts = dict(
        config=config,
    )
    return dict(layouts=layouts)
