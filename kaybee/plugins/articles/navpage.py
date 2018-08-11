"""

Combine the functionality of menus and sidebar multi-level nav,
like in bulma.io

Navpages can be used:

- As a menu with a default link and submenu entries

- A secondary navigation scheme, manually-encoded

"""
from typing import List

from pydantic import BaseModel

from kaybee.app import kb

from kaybee.plugins.articles.base_section import BaseSection, BaseSectionModel
from plugins.queries.props_model import BaseQueryModel


class MenuEntryModel(BaseModel):
    docname: str
    label: str = None
    subheading: str = None
    accent: str = 'primary'
    icon: str = 'fas fa-eye'
    query: BaseQueryModel = None


class NavpageModel(BaseSectionModel):
    entries: List[MenuEntryModel]


@kb.resource('navpage')
class Navpage(BaseSection):
    props: NavpageModel

    def entries(self, resources):
        results = []
        for entry in self.props.entries:
            # Get the resource for this entry
            result = {}
            resource = resources[entry.docname]
            result['label'] = entry.label if entry.label else resource.title

            # Subheading can come from several places
            if getattr(entry, 'subheading', False):
                result['subheading'] = entry.subheading
            else:
                subheading = getattr(resource.props, 'subheading', '')
                if subheading is None:
                    subheading = ''
                result['subheading'] = subheading

            results.append(result)

        return results
