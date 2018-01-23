from typing import List

from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent


@kb.event(SphinxEvent.EBRD, scope='queries', system_order=40)
def initialize_query_service(kb_app: kb,
                             sphinx_app: Sphinx,
                             sphinx_env: BuildEnvironment,
                             docnames=List[str],
                             ):
    # TODO Doesn't look like this is needed
    sphinx_app.query = dict()
