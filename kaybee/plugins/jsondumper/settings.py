from pydantic import BaseModel


class JsondumperModel(BaseModel):
    use_jsondump: bool = False

    class Config:
        ignore_extra = False
