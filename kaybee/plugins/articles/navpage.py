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
from kaybee.plugins.queries.props_model import BaseQueryModel
from kaybee.plugins.queries.service import Query


class MenuEntryModel(BaseModel):
    docname: str
    label: str = None
    subheading: str = None
    accent: str = 'primary'
    icon: str = 'fas fa-eye'
    query: BaseQueryModel = None


class NavpageModel(BaseSectionModel):
    entries: List[MenuEntryModel] = []


@kb.resource('navpage')
class Navpage(BaseSection):
    props: NavpageModel

    def entries(self, resources, references):
        results = []
        for entry in self.props.entries:
            # Get the resource for this entry
            resource = resources[entry.docname]

            result = dict(
                docname=entry.docname,
                entries=[],
                entries_count=0,
            )
            result['label'] = entry.label if entry.label else resource.title

            # Subheading can come from several places
            if getattr(entry, 'subheading', False):
                result['subheading'] = entry.subheading
            else:
                subheading = getattr(resource.props, 'subheading', '')
                if subheading is None:
                    subheading = ''
                result['subheading'] = subheading

            # Accent and icon
            result['accent'] = entry.accent
            result['icon'] = entry.icon

            # Process the query, if any
            query = entry.query
            if query:
                query_results = Query.filter_collection(
                    resources,
                    rtype=query.rtype,
                    props=query.props,
                    parent_name=query.parent_name,
                    sort_value=query.sort_value,
                    limit=query.limit,
                    reverse=query.reverse
                )

                # Flatten the query results
                for r in query_results:
                    result['entries'].append(dict(
                        title=r.title,
                        label=r.title,
                        rtype=r.rtype,
                        excerpt=r.excerpt,
                        docname=r.docname,
                        duration=r.props.duration,
                        published=r.props.published,
                        accent='primary',
                        icon='fas fa-eye',
                        author=r.get_author(references),
                        references=r.get_references(references),
                        logo=r.get_logo(resources)
                    ))
                result['entries_count'] = len(query_results)

            results.append(result)

        return results
