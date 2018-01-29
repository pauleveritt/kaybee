from typing import Dict

from pydantic import ValidationError
from ruamel.yaml import load, Loader
from sphinx.errors import SphinxError


def load_model(docname: str, model, yaml_content: str) -> Dict:
    # If yaml_content is an empty string and parses to None, return
    # empty dic instead
    yaml_props = (load(yaml_content, Loader=Loader) or {})

    # Make the model, which validates, then do any extra validation
    try:
        m = model(**yaml_props)
    except ValidationError as exc:
        msg = f'Validation error in docname {docname}: {exc}'
        raise SphinxError(msg)
    return m
