from typing import Optional

from pydantic import BaseModel
from sphinx.application import Sphinx


class BaseLayoutModel(BaseModel):
    pass


class BaseLayout:
    model = BaseLayoutModel

    def __init__(self, **kwargs):
        self.settings = self.model(**kwargs)
        self.sphinx_app: Optional[Sphinx] = None
