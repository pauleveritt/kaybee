from sphinx.application import Sphinx

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent


@kb.event(SphinxEvent.BI, scope='resources')
def handle_builderinited(kb_app: kb, sphinx_app: Sphinx):
    pass
