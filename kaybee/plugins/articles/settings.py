from pydantic import BaseModel


class ArticlesModel(BaseModel):
    use_toctree: bool = False

    class Config:
        ignore_extra = False
