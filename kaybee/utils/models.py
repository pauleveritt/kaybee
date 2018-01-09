from typing import Dict

from ruamel.yaml import load, Loader


def load_model(model, yaml_content: str) -> Dict:
    # If yaml_content is an empty string and parses to None, return
    # empty dic instead
    yaml_props = (load(yaml_content, Loader=Loader) or {})

    # Make the model, which validates, then do any extra validation
    m = model(**yaml_props)

    return m
