from typing import List

from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.references.container import ReferencesContainer


@kb.event(SphinxEvent.EBRD, scope='references', system_order=40)
def initialize_references_container(kb_app: kb,
                                    sphinx_app: Sphinx,
                                    sphinx_env: BuildEnvironment,
                                    docnames=List[str],
                                    ):
    sphinx_app.references = ReferencesContainer()


@kb.event(SphinxEvent.EBRD, 'references', system_order=50)
def register_references(kb_app: kb,
                        sphinx_app: Sphinx,
                        sphinx_env: BuildEnvironment,
                        docnames: List[str]):
    """ Walk the registry and add sphinx directives """

    references: ReferencesContainer = sphinx_app.references

    for name, klass in kb_app.config.references.items():
        # Name is the value in the decorator and directive, e.g.
        # @kb.reference('category') means name=category
        if getattr(klass, 'is_reference', False):
            references[name] = dict()


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
