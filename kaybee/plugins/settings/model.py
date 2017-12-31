from pydantic import BaseModel

from kaybee.plugins.debugdumper.model import DebugdumperModel


class KaybeeSettings(BaseModel):
    debugdumper: DebugdumperModel = DebugdumperModel()
