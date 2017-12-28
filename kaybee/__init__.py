__version__ = '0.0.7'
__title__ = "kaybee"


def setup(app):
    """ Initialize Kaybee as a Sphinx extension """

    return dict(
        version=__version__,
        parallel_read_safe=False
    )
