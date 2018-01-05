from kaybee.app import kb
from kaybee.plugins.genericpage.genericpage import Genericpage


@kb.genericpage()
class MyGenericpage(Genericpage):
    def hello(self):
        return 'world'
