"""

An out-of-the-box toctree type.

"""

from kaybee.app import kb

from kaybee.plugins.articles.base_toctree import BaseToctree

# When no context argument is supplied, it sets the default
# toctree handler


@kb.toctree(system_order=80)
class Toctree(BaseToctree):
    pass
