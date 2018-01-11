"""
New types that can be used in pydantic models.

"""


class ReferencesType(str):
    @classmethod
    def get_validators(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, list):
            raise ValueError(f'reference: expected list, not {type(v)}')
        for i in v:
            if not isinstance(i, str):
                prefix = 'reference: expected list of strings, '
                msg = f'{prefix} not {type(i)}'
                raise ValueError(msg)
        return v
