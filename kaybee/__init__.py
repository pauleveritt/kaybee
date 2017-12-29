from sphinx.application import Sphinx

from kaybee.app import kb
from kaybee.plugins.events import EventAction

__version__ = '0.0.7'
__title__ = "kaybee"


def setup(app: Sphinx):
    """ Initialize Kaybee as a Sphinx extension """

    app.connect('builder-inited',
                lambda sphinx_app: EventAction.call_builder_init(kb,
                                                                 sphinx_app))

    return dict(
        version=__version__,
        parallel_read_safe=False
    )
