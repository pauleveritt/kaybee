from typing import List

from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.resources.container import ResourcesContainer


@kb.event(SphinxEvent.EBRD, scope='references', system_order=40)
def initialize_resources_container(kb_app: kb,
                                   sphinx_app: Sphinx,
                                   sphinx_env: BuildEnvironment,
                                   docnames=List[str],
                                   ):
    sphinx_app.resources = ResourcesContainer()


@kb.event(SphinxEvent.EBRD, 'references', system_order=50)
def register_references(kb_app: kb,
                        sphinx_app: Sphinx,
                        sphinx_env: BuildEnvironment,
                        docnames: List[str]):
    """ Walk the registry and add sphinx directives """

    pass


@kb.event(SphinxEvent.ECC, 'references')
def validate_references(kb_app: kb,
                        sphinx_builder: StandaloneHTMLBuilder,
                        sphinx_env: BuildEnvironment):
    pass


@kb.event(SphinxEvent.MR, 'references')
def missing_reference(kb_app: kb,
                      sphinx_env: BuildEnvironment,
                      node,
                      contnode):
    pass
