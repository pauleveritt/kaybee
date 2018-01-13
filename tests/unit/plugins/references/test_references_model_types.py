import pytest

from kaybee.plugins.references.model_types import ReferencesType


class TestReferencesType:
    def test_import(self):
        assert 'ReferencesType' == ReferencesType.__name__

    def test_get_validators(self):
        validators = ReferencesType.get_validators()
        assert ReferencesType.validate == list(validators)[0]

    def test_validate_not_list(self):
        reference_value = 9
        with pytest.raises(ValueError):
            ReferencesType.validate(reference_value)

    def test_validate_not_list_of_strings(self):
        reference_value = [9, 9]
        with pytest.raises(ValueError):
            ReferencesType.validate(reference_value)

    def test_validate_list_of_strings(self):
        reference_value = ['9', '10']
        results = ReferencesType.validate(reference_value)
        assert reference_value == results
