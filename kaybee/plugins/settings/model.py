from pydantic import BaseModel

from kaybee.plugins.debugdumper.settings import DebugdumperModel


class KaybeeSettings(BaseModel):
    plugins_dir: str = 'kaybee_plugins'
    debugdumper: DebugdumperModel = DebugdumperModel()
