from typing import Dict, Mapping

from pydantic import BaseModel
from ruamel.yaml import load, Loader


def parse_parent(docname):
    """ Given a docname path, pick apart and return name of parent """

    lineage = docname.split('/')
    lineage_count = len(lineage)

    if docname == 'index':
        # This is the top of the Sphinx project
        parent = None
    elif lineage_count == 1:
        # This is a non-index doc in root, e.g. about
        parent = 'index'
    elif lineage_count == 2 and lineage[-1] == 'index':
        # This is blog/index, parent is the root
        parent = 'index'
    elif lineage_count == 2:
        # This is blog/about
        parent = lineage[0] + '/index'
    elif lineage[-1] == 'index':
        # This is blog/sub/index
        parent = '/'.join(lineage[:-2]) + '/index'
    else:
        # This should be blog/sub/about
        parent = '/'.join(lineage[:-1]) + '/index'

    return parent


def load_model(model, yaml_content: str) -> Dict:
    # If yaml_content is an empty string and parses to None, return
    # empty dic instead
    yaml_props = (load(yaml_content, Loader=Loader) or {})

    # Make the model, which validates, then do any extra validation
    m = model(**yaml_props)

    return m


class BaseResourceModel(BaseModel):
    """ Kaybee default schema definitions for resources """

    template: str = None
    acquireds: Mapping[str, Mapping[str, str]] = None
    excerpt: str = None
    auto_excerpt: int = 1


class BaseResource:
    model = BaseResourceModel
    json_attrs = ('docname', 'rtype', 'parent')

    def __init__(self, docname: str, rtype: str, yaml_content: str):
        self.docname = docname
        self.rtype = rtype
        self.parent = parse_parent(docname)
        self.props = load_model(self.model, yaml_content)

    def __repr__(self):
        return self.docname

    def parents(self, resources):
        """ Split the path in name and get parents """

        if self.docname == 'index':
            # The root has no parents
            return []
        parents = []
        parent = resources.get(self.parent)
        while parent is not None:
            parents.append(parent)
            parent = resources.get(parent.parent)
        return parents

    @property
    def __json__(self):
        return dict(
            docname=self.docname,
            rtype=self.rtype,
            parent=self.parent,
            props=self.props.values()
        )

    def find_prop(self, resources, prop_name):
        """ Starting with self, walk until you find prop or None """

        # Instance
        custom_prop = getattr(self.props, prop_name, None)
        if custom_prop:
            return custom_prop

        # Parents...can't use find_prop as have to keep going on acquireds
        for parent in self.parents(resources):
            acquireds = parent.props.acquireds
            if acquireds:
                # First try in the per-type acquireds
                rtype_acquireds = acquireds.get(self.rtype)
                if rtype_acquireds:
                    prop_acquired = rtype_acquireds.get(prop_name)
                    if prop_acquired:
                        return prop_acquired

                # Next in the "all" section of acquireds
                all_acquireds = acquireds.get('all')
                if all_acquireds:
                    prop_acquired = all_acquireds.get(prop_name)
                    if prop_acquired:
                        return prop_acquired

        return

    def template(self, resources):
        """ Get the template from: YAML, hierarchy, or class """

        template_name = self.find_prop(resources, 'template')
        if template_name:
            return template_name
        else:
            return self.__class__.__name__.lower()
