from kaybee.app import kb
from kaybee.plugins.articles.base_toctree import BaseToctree


@kb.toctree(system_order=40)
class MyToctree(BaseToctree):
    template = 'mytoctree'
