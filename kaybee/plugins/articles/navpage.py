"""

Combine the functionality of menus and sidebar multi-level nav,
like in bulma.io

Navpages can be used:

- As a menu with a default link and submenu entries

- A secondary navigation scheme, manually-encoded

"""
from typing import List

from pydantic import BaseModel
from sphinx.util import relative_uri

from kaybee.app import kb

from kaybee.plugins.articles.base_section import BaseSection, BaseSectionModel
from kaybee.plugins.queries.props_model import BaseQueryModel
from kaybee.plugins.queries.service import Query

PYTHON_LOGO = 'https://cdn.worldvectorlogo.com/logos/python-5.svg'

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

    def _get_author(self, resource, references):
        # Used by section_entries to make the listing of links resources
        # as "tags"
        resource_references = resource.props.references
        if resource_references:
            if 'author' in resource_references:
                pa_label = resource_references['author'][0]
                pa = references["author"][pa_label]
                images = pa.props.images
                first_image = images[0].filename if images else None
                author_href = relative_uri(resource.docname, pa.docname)
                thumbnail_url = author_href + '/../' + first_image
                author = dict(
                    title=pa.title,
                    href=author_href,
                    thumbnail_url=thumbnail_url,
                )
                return author

    def _get_references(self, resource, references):
        # Used by section_entries to make the listing of links resources
        # as "tags"
        # Used by section_entries to make the listing of links resources
        # as "tags"

        resource_references = resource.props.references
        if resource_references:
            # Handle all non-author references for tag-like links
            these_references = []
            for reftype, labels in resource_references.items():
                this_reftype = references[reftype]
                if reftype != 'author':
                    for label in labels:
                        this_ref = this_reftype[label]
                        this_href = relative_uri(resource.docname,
                                                 this_ref.docname)
                        these_references.append(
                            dict(
                                label=label,
                                href=this_href,
                            )
                        )
            return these_references

    def _get_logo(self, resource, resources):
        # Find the primary_reference logo
        primary_reference = resource.props.primary_reference
        if not primary_reference:
            return PYTHON_LOGO
        reference_resource = resources[primary_reference]
        logo = reference_resource.props.logo
        return logo if logo else PYTHON_LOGO

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
                        rtype=r.rtype,
                        excerpt=r.excerpt,
                        docname=r.docname,
                        duration=r.props.duration,
                        published=r.props.published,
                        accent='primary',
                        icon='fas fa-eye',
                        author=self._get_author(r, references),
                        references=self._get_references(r, references),
                        logo=self._get_logo(r, resources)

                    ))
                result['entries_count'] = len(query_results)

            results.append(result)

        return results
