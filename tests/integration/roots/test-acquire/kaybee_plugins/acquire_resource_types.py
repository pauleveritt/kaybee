from kaybee.app import kb

from kaybee.plugins.resources.base_resource import BaseResource


@kb.resource('article')
class Article(BaseResource):
    pass


@kb.resource('homepage')
class Homepage(BaseResource):
    pass


@kb.resource('section')
class Section(BaseResource):
    pass
