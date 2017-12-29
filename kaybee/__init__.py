from sphinx.application import Sphinx

from kaybee.app import kb
from kaybee.plugins.events import EventAction, SphinxEvent

__version__ = '0.0.7'
__title__ = "kaybee"


def setup(app: Sphinx):
    """ Initialize Kaybee as a Sphinx extension """

    app.connect(SphinxEvent.BI.value,
                lambda sphinx_app: EventAction.call_builder_init(
                    kb, sphinx_app)
                )
    app.connect(SphinxEvent.EPD.value,
                lambda sphinx_app, env, docname: EventAction.call_purge_doc(
                    kb, sphinx_app, env, docname)
                )

    app.connect(SphinxEvent.EBRD.value,
                lambda sphinx_app, env,
                       docnames: EventAction.call_env_before_read_docs(
                    kb, sphinx_app, env, docnames)
                )

    app.connect(SphinxEvent.DREAD.value,
                lambda sphinx_app, doctree: EventAction.call_env_doctree_read(
                    kb, sphinx_app, doctree)
                )

    return dict(
        version=__version__,
        parallel_read_safe=False
    )
