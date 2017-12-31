from pydantic import BaseModel

from plugins.debugdumper.model import DebugdumperModel


class KaybeeSettings(BaseModel):
    debugdumper: DebugdumperModel = None
