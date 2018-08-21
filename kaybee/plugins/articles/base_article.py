from datetime import datetime
from typing import List

from sphinx.util import relative_uri

from kaybee.plugins.articles.image_type import ImageModel
from kaybee.plugins.resources.base_resource import (
    BaseResource,
    BaseResourceModel
)


class BaseArticleModel(BaseResourceModel):
    style: str = None
    css_class: str = None
    in_nav: bool = False
    nav_title: str = None
    weight: int = 0
    published: datetime = None
    excerpt: str = None
    auto_excerpt: int = 1
    images: List[ImageModel] = []
    is_series: bool = False
    duration: str = None
    primary_reference: str = None
    icon: str = 'fas fa-eye'
    accent: str = 'primary'


class BaseArticle(BaseResource):
    props: BaseArticleModel
    excerpt: str = None  # Stamped on later by the handler
    toctree: List[str] = []  # Stamped on later by the handler

    def section(self, resources):
        """ Which section is this in, if any """

        section = [p for p in self.parents(resources) if p.rtype == 'section']
        if section:
            return section[0]
        return None

    def in_navitem(self, resources, nav_href):
        """ Given  href of nav item, determine if resource is in it """

        # The navhref might end with '/index' so remove it if so
        if nav_href.endswith('/index'):
            nav_href = nav_href[:-6]

        return self.docname.startswith(nav_href)

    @property
    def is_published(self):
        """ Return true if this resource has published date in the past """

        now = datetime.now()
        published = self.props.published
        if published:
            return published < now
        return False

    def steps(self, resources):
        return self.parents(resources)[0].toctree

    def series(self, resources):
        # Make sure the parent is a registered resource
        parent = resources.get(self.parent)
        if not parent:
            return None

        # The parent has to declare that it wants to have its children
        # in a "series", which is false by default.
        if not getattr(parent.props, 'is_series', False):
            return None

        results = []
        for docname in parent.toctree:
            resource = resources.get(docname)
            if resource:
                # We might have a non-resource page in the toctree,
                # so skip it if true
                excerpt = getattr(resource, 'excerpt', False)
                results.append(
                    dict(
                        docname=docname,
                        title=resource.title,
                        excerpt=excerpt,
                        current=self.docname == docname
                    )
                )
        return results

    def breadcrumbs(self, resources):
        entries = [
            dict(
                label=r.title,
                docname=r.docname
            )
            for r in self.parents(resources)[:-1]
        ]
        entries.reverse()
        entries.insert(0, dict(label='Home', docname='/index'))
        entries.append(dict(
            label=self.title, docname=self.docname, is_active=True))
        return entries

    def get_author(self, references):
        # Used by section_entries to make the listing of links resources
        # as "tags"
        resource_references = self.props.references
        if resource_references:
            if 'author' in resource_references:
                pa_label = resource_references['author'][0]
                pa = references["author"][pa_label]
                images = pa.props.images
                first_image = images[0].filename if images else None
                author_href = relative_uri(self.docname, pa.docname)
                thumbnail_url = author_href + '/../' + first_image
                author = dict(
                    title=pa.title,
                    href=author_href,
                    thumbnail_url=thumbnail_url,
                )
                return author

    def get_references(self, references):
        # Used by section_entries to make the listing of links resources
        # as "tags"
        # Used by section_entries to make the listing of links resources
        # as "tags"

        resource_references = self.props.references
        if resource_references:
            # Handle all non-author references for tag-like links
            these_references = []
            for reftype, labels in resource_references.items():
                this_reftype = references[reftype]
                if reftype != 'author':
                    for label in labels:
                        this_ref = this_reftype[label]
                        this_href = relative_uri(self.docname,
                                                 this_ref.docname)
                        these_references.append(
                            dict(
                                label=label,
                                href=this_href,
                            )
                        )
            return these_references

    def get_logo(self, resources):
        # Find the primary_reference logo
        PYTHON_LOGO = 'https://cdn.worldvectorlogo.com/logos/python-5.svg'
        primary_reference = self.props.primary_reference
        if not primary_reference:
            return PYTHON_LOGO
        reference_resource = resources[primary_reference]
        logo = reference_resource.props.logo
        return logo if logo else PYTHON_LOGO

    def __json__(self, resources):
        d = super().__json__(resources)
        if self.excerpt:
            d['excerpt'] = self.excerpt
        section = getattr(self.section(resources), 'docname', '')
        if section:
            d['section'] = section
        if self.toctree:
            d['toctree'] = self.toctree
        if self.series:
            d['series'] = self.series(resources)

        return d
