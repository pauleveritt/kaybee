from pydantic import BaseModel


class BaseWidgetModel(BaseModel):
    template: str


class BaseWidget:
    def __init(self, *args):
        pass
