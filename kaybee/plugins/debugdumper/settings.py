from pydantic import BaseModel


class DebugdumperModel(BaseModel):
    use_debug: bool = False
