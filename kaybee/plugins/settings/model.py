from pydantic import BaseModel

from kaybee.plugins.articles.settings import ArticlesModel
from kaybee.plugins.debugdumper.settings import DebugdumperModel


class KaybeeSettings(BaseModel):
    plugins_dir: str = 'kaybee_plugins'
    articles: ArticlesModel = ArticlesModel()
    debugdumper: DebugdumperModel = DebugdumperModel()

    class Config:
        ignore_extra = False
