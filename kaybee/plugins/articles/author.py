from pathlib import Path

from kaybee.app import kb
from kaybee.plugins.articles.base_article_reference import BaseArticleReference


@kb.resource('author')
class Author(BaseArticleReference):
    def headshot_thumbnail(self, usage):
        docpath = Path(self.docname)
        parent = docpath.parent
        prop = self.find_prop_item('images', 'usage', usage)
        return str(Path(parent, prop.filename))  # prop.filename
