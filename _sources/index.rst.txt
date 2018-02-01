kaybee Static Sites for Knowledge Bases
=======================================

Static websites are a nice way to publish content. Sometimes, though, the
content is...well...content. There's data in there, and you'd like a
static website oriented around information and structure, aka a knowledge
base.

Kaybee is a Knowledge Base (KB, kaybee) in which you can define kinds of
content then put the data into your documents. You can then easily embed
query-driven listings into your content to organize your knowledge base.

Kaybee is based on `Sphinx <http://www.sphinx-doc.org/en/stable/>`_, the
well-known Python tool for richly-interlinked content.

Not sure what this means? Here's a simple "article" resource, as a Sphinx
``.rst`` document:

.. code-block:: rst

    .. article::
        style: research_section
        in_nav: True
        weight: 30
        published: 2018-01-01 12:23
        category:
            - category1
            - category2
        auto_excerpt: 2

    =========
    Article 1
    =========

    Some text.

Want to see more: Jump over to :doc:`using/index` for details.

Features
========

Kaybee adds a lot to Sphinx:

- Turn pages into resources with YAML embedded into the text

- Resources can be defined with a schema that validates the YAML

- Custom templates can be associated with resource types, individual pages,
  or whole parts of the site

- The folder structure goes into the resource data model (parents)

- Properties from the YAML can be pushed up the site to parent directories,
  making it easy to share data

- Custom widgets can use a query service to select and render resources, in
  the middle of a page

- A reference system lets you define a vocabulary using resources, then
  refer to that vocabulary from YAML or inline (with exceptions raised when
  references don't exist)

- An built-in article system adds a system of articles, sections, home pages,
  content listings, publishing policies, and more

Kaybee also puts a new, modern, powerful, simple layer atop Sphinx's
extension model. This makes it easy to extend Kaybee:

- Make new kinds of resources with a simple Python class (which is available
  in the template)

- Transparently associate a Jinja2 template with a resource type

- Associate PEP-484 "models" with resource types for validation

- Extend the site settings to give users validated knobs for settings

- Define a reference system such as author, category, tag, etc. using simple
  Python classes

- Handle Sphinx events, register Sphinx directives, and more

Kaybee also has some related projects. Primarily, a layout based on
`Bulma <https://bulma.io>`_ with some interesting approaches.

Additionally, Kaybee has a *lot* of unit tests (usually at or close to
100% coverage) and integration tests (usually over 90%.)

Contents
========

.. toctree::
    :maxdepth: 2

    whysphinx
    using/index
    extending/index
    development/index
    implementation/index
