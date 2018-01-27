from kaybee.app import kb
from kaybee.plugins.articles.base_toctree import BaseToctree


@kb.toctree(system_order=70)
class MyToctree(BaseToctree):
    pass
