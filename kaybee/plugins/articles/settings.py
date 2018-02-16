from pydantic import BaseModel


class ArticlesModel(BaseModel):
    use_toctree: bool = False
    datefmt_short: str = '%b %d'
    datefmt_long: str = '%Y/%m/%d'
    datefmt_full: str = '%Y/%m/%d %H:%M'

    class Config:
        ignore_extra = False
