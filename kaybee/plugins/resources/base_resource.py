from typing import Mapping, List

from pydantic import BaseModel

from kaybee.utils.models import load_model


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

    return parent  # This is a path


class BaseResourceModel(BaseModel):
    """ Kaybee default schema definitions for resources """

    template: str = None
    acquireds: Mapping[str, Mapping[str, str]] = None
    references: Mapping[str, List[str]] = dict()

    class Config:
        ignore_extra = False


class BaseResource:
    json_attrs = ('docname', 'rtype', 'parent')
    title: str = None  # Stamped on later by the handler
    props: BaseResourceModel

    def __init__(self, docname: str, rtype: str, yaml_content: str):
        self.docname = docname
        self.rtype = rtype
        self.parent = parse_parent(docname)

        model = self.__annotations__['props']
        self.props = load_model(docname, model, yaml_content)

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

    def acquire(self, resources, prop_name):
        """ Starting with self, walk until you find prop or None """

        # Instance
        custom_prop = getattr(self.props, prop_name, None)
        if custom_prop:
            return custom_prop

        # Parents...can't use acquire as have to keep going on acquireds
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

        template_name = self.acquire(resources, 'template')
        if template_name:
            return template_name
        else:
            # We're putting an exception for "resource", the built-in
            # rtype/directive. We want it to work out-of-the-box without
            # requiring an _templates/resource.html in the docs project.
            # Instead, use the page.html the ships with Sphinx.
            if self.rtype == 'resource':
                return 'page'
            else:
                return self.rtype

    def __json__(self, resources):
        # The root has different rules about parents
        if self.docname == 'index':
            parent_docnames = self.parents(resources)
        else:
            parent_docnames = [p.docname for p in
                               self.parents(resources)]
        return dict(
            docname=self.docname,
            title=self.title,
            parent_docnames=parent_docnames,
            template=self.template(resources),
            rtype=self.rtype,
            parent=self.parent,
            props=self.props.dict(),
            repr=repr(self),
        )
