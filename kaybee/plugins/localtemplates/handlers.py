import os
from typing import List

from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.jinja2glue import SphinxFileSystemLoader

from kaybee.app import kb

from kaybee.plugins.events import SphinxEvent


@kb.event(SphinxEvent.EBRD, scope='localtemplates')
def handle_beforereaddocs(kb_app: kb, sphinx_app: Sphinx,
                          sphinx_env: BuildEnvironment,
                          docnames: List[str]):
    confdir = os.path.join(sphinx_app.confdir, '_templates')
    template_bridge = sphinx_app.builder.templates
    template_bridge.loaders.insert(0, SphinxFileSystemLoader(confdir))
