from kaybee.app import kb
from kaybee.plugins.articles.base_article_reference import BaseArticleReference


@kb.resource('author')
class Author(BaseArticleReference):
    def headshot_thumbnail(self, usage):
        prop = self.find_prop_item('images', 'usage', usage)
        return prop.filename
