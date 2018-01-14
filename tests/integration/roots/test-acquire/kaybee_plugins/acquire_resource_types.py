from kaybee.app import kb

from kaybee.plugins.resources.base_resource import BaseResource


@kb.resource('aqarticle')
class Article(BaseResource):
    pass


@kb.resource('aqhomepage')
class Homepage(BaseResource):
    pass


@kb.resource('aqsection')
class Section(BaseResource):
    pass
