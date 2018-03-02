.. homepage::

    published: 2018-01-01 12:23
    heading: Kaybee
    subheading: Extensible Knowledge Base for Static Sites
    hero_image: library.jpg
    style: dark

kaybee Static Sites for Knowledge Bases
=======================================

.. sectionbox::
    name: sbhero
    style: splash

    Static websites are a nice way to publish content. Sometimes,
    though, the content is...well...content. There's data in there,
    and you'd like a static website oriented around information and
    structure.

    Kaybee is a Knowledge Base (KB, kaybee) in which you define
    kinds of content, put the data in your docs, then do neat stuff.

.. featuretiles::
    name: featuretiles1
    rows:
        - - heading: Key Features
            bullets:
                - Built on the powerful, mature Sphinx documentation
                  system
                - Turn pages into resources with YAML embedded into the text
                - Validate that YAML with custom schemas
                - Associate templates with resources or individual pages
                - Inline widgets to query the documents and render output
                - Extensible references to connect resources
                - Built-in article system, ready-to-go, out-of-the-box
            style: is-primary
            more_href: features
          - heading: Resources
            subheading: Embed YAML in pages to make resources.
            bullets:
                - Use a special Sphinx directive to put some YAML at the top of your
                  document
                - Kaybee then records this in a Python database in your app
                - Use out-of-the-box directives or write classes to make your own
                  resources using a simple decorator on a Python class
                - Access the resource in your Jinja2 template
                - Your Sphinx folder structure is available as a resource tree
            style: is-info
            more_href: using/resources
          - heading: Schemas
            subheading: Some third feature text.
            style: is-warning
            more_href: using/schemas
            bullets:
                - YAML is validated against schemas
                - Write schemas as PEP-484 Python classes using
                  pydantic
                - Associate these schemas with your resource type definitions
                - Access these as resource "properties" in your Jinja2 templates or
                  widget queries
                - Push some properties to parents in the resource tree, to control
                  whole sections of the site
        - - heading: Templates
            subheading: Some fourth feature text.
            style: is-primary
            more_href: using/templates
            bullets:
                - Write Jinja2 templates for your resources, widgets, and more
                - Assign a template to a specific resource via YAML, or a section of
                  your site, or for all resources in a class
                - Associate a template with a specific widget on a certain page
                - Easily customize the data available in a template
          - heading: Widgets
            subheading: Some fifth feature text.
            style: is-info
            more_href: using/widgets
            bullets:
                - Have a custom, data-driven box in the middle of a document
                - Use existing widgets or easily register your own, with associated
                  YAML schema and template
                - Express a query in YAML which collects resources from the Python
                  collection and renders in a custom template
          - heading: References
            subheading: Some sixth feature text.
            style: is-warning
            more_href: using/references
            bullets:
                - Use an existing reference system or define your own, such as tags or
                  authors
                - Associate documents as entries in that reference system with simple
                  YAML at the top
                - Then tag a resource as being in that category using reference-validated
                  YAML
                - Easily interate over forward and backwards references in templates
                - Make inline-linking references in content using the Sphinx syntax
        - - heading: Articles
            subheading: Some fourth feature text.
            style: is-primary
            more_href: using/articles
            bullets:
                - A ready-to-go publishing system with resources, widgets, references,
                  and more
                - Articles with publication date filtering
                - Widgets which query the resources in interesting ways
          - heading: Extensibility
            subheading: Some fifth feature text.
            style: is-info
            more_href: extending/index
            bullets:
                - some points
          - heading: Sphinx
            subheading: Some sixth feature text.
            style: is-warning
            bullets:
                - Built on the mature static-site-generator used for ReadTheDocs and
                  Python
                - Sphinx provides rich facilities for organizing and extending your
                  content
                - Kaybee is a layer atop Sphinx that provides a simpler extension model


Contents
========

.. toctree::
    :hidden:

    whysphinx
    features
    using/index
    articles/index
    extending/index
    development/index
    implementation/index
    categories/index
