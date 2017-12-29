from kaybee.plugins.events import EventAction
__version__ = '0.0.7'
__title__ = "kaybee"


def setup(app):
    """ Initialize Kaybee as a Sphinx extension """

    app.connect('builder-inited', EventAction.call_builder_init)

    return dict(
        version=__version__,
        parallel_read_safe=False
    )
