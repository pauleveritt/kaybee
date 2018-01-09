from typing import List, Any

from pydantic import BaseModel


class CorePropFilterModel(BaseModel):
    key: str
    value: Any


class BaseQueryModel(BaseModel):
    rtype: str = None
    limit: int = None
    parent_name: str = None
    sort_value: str = 'title'
    reverse: bool = False
    props: List[CorePropFilterModel] = []
