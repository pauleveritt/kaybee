from kaybee.utils.models import load_model

from pydantic import BaseModel


class FakeModel(BaseModel):
    flag: int = None


class TestLoadModel:
    def test_import(self):
        assert 'load_model' == load_model.__name__

    def test_load(self):
        content = 'flag: 99'
        actual = load_model(FakeModel, content)
        assert actual.flag == 99
