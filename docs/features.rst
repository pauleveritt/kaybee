.. article::
    published: 2018-01-02 12:01
    in_nav: True
    weight: 10

========
Features
========

Kaybee is a *static site generator* for knowledge bases. Like other static
site generators, it makes it easy to author content which then
generate HTML files. No database, no application server, easy-peasy.

Kaybee is based on :doc:`Sphinx <sphinx:intro>`, the system behind
`ReadTheDocs <https://readthedocs.org>`_. Sphinx is a very powerful, mature,
Python system for richly interlinked documentation and content.

Kaybee adds a lot to Sphinx. This document covers the main features.

.. _features-resources:

Resources
=========

Sphinx has documents. Meaning. ``.rst`` files in a folder on disk which
are included into a :ref:`table of contents <sphinx:toctree-directive>` in
some parent document.

Kaybee turns these documents into *resources*. By sprinkling some metadata
at the top, you create a resource stored in a Python object that can be
then queried like a database.

- Custom ``resource`` Sphinx :ref:`directive <sphinx:directives>`

- The body of the directive is YAML

- The YAML (and other properties) get stored on the Sphinx app object
  under ``resources``

- The YAML can name a custom Jinja2 template for this document

- Use Kaybee's :doc:`acquired properties <./using/acquireds>` to centralize
  properties in rich ways

Let's say I had a Sphinx page such as the root of a docs project:

.. code-block:: rst

    Hello World
    ===========

What does it take to turn this document into a "resource"? Kaybee ships
with a Sphinx directive ``resource`` which you can use:

.. code-block:: rst

    .. resource::

    Hello World
    ===========

I have now turned this document into a "resource" of resource type "resource".

Let's say, for this particular document, I want a different template. Here
is the YAML:

.. code-block:: rst

    .. resource::
        template: mypage

    Hello World
    ===========

Kaybee will now look for a Jinja2 template named ``mypage.html`` in one of
Sphinx's registered directories.

Let's give a sneak peek at writing your own "kinds of things". This Python
makes a ``ksresource`` resource:

.. literalinclude:: ../tests/integration/roots/test-kitchensink/kaybee_plugins/kitchensink_custom.py
    :start-after: # Start KsResource Model and Class
    :end-before: # End KsResource Model and Class

Your docs can now have a ``ksresource`` directive, which has validated YAML
that can use a ``ksresource_flag`` integer, with a ``ksresource.html``
template. That template can refer to ``resource`` as a variable, which is an
instance of this class, and thus ``resource.increment`` is available in the
template (along with a ``resource.props.ksresource_flag`` property.)

Schemas
=======

Resources are a directive that encodes properties in YAML. That YAML is
validated against a schema. Kaybee has a rich schema system:

- Uses :ref:`category-pydantic` for validation

- Schemas are written as Python PEP-484 type annotated classes

- YAML data is validated against that schema into a Python data structure
  as properties

- Properties are stored on the resource and available for querying by
  widgets or use in templates

For example, ``resource`` expects an optional ``template`` string. Let's say
a document has this:

.. code-block:: rst

    .. resource::
        template: 999

    Hello World
    ===========

When you run Sphinx, Kaybee throws a validation error because template is
expected to be a string.

Templates
=========

Sphinx uses Jinja2 as its template engine and provides a layered approach
to where templates can be found. Kaybee extends this by making it easy
to associate templates to documents in powerful ways.

- Uses the popular Jinja2 template engine

- Assign a template for a single resource, a classs or resources, or
  sections of the site (using acquired properties)

- Kaybee includes more variables in the template scope (e.g. the current
  resource or widget)

- Works either with "normal" Sphinx themes or approaches like
  ``kaybee_bulma`` which uses a new set of Jinja2 templates

For example, in the code block above:

.. code-block:: rst

    .. resource::
        template: mypage

    Hello World
    ===========

An author could then create a Jinja2 file at ``_templates/mypage.html``.
This template could reference variables on the resource such as
``{{ resource.title }}``, ``{{ resource.excerpt }}``, or
``{{ resource.props.template.title }}``.

Widgets
=======

Widgets make it easy to create configurable directives that appear in the
middle of the page and render HTML. The widgets can provide a template,
a schema, and a class.

For example, we collect resources with metadata into a Python object at
``sphinx_app.env.resources``. What can we do with it? We can use the built-in
``widget`` directive:

.. literalinclude:: ../tests/integration/roots/test-widgets1/index.rst
    :language: rst

We can then define a template at ``_templates/widgets2_hello``:

.. literalinclude:: ../tests/integration/roots/test-widgets1/_templates/widgets2_hello.html
    :start-after: resource_docname3

Kaybee provides directive support for "querying" the resources from the
widget's YAML:

.. literalinclude:: ../tests/integration/roots/test-kitchensink/2017/index.rst
    :language: rst
    :start-after: Here is a query
    :lines: 2-6

The query can specify different kinds of property filtering, sorting,
limiting, and more.

For more power, you can write a custom widget as a Python class with a
custom YAML schema and associated template:

.. literalinclude:: ../tests/integration/roots/test-widgets2/kaybee_plugins/listing_widget.py

When this module is imported, your docs can use a ``listing`` widget which
adds ``another_flag`` to the Jinja2 execution context.

References
==========

Sphinx provides a number of useful, powerful ways to link content. With
resources, what can Kaybee do?

First, Kaybee's :doc:`../articles/index` ships with a "category" reference
system. You can make a resource -- a Sphinx document -- that also acts as a
category value, for example for a ``django``:

.. literalinclude:: ../tests/integration/roots/test-kitchensink/categories/django.rst
    :language: rst

Other documents can now reference that category:

.. literalinclude:: ../tests/integration/roots/test-kitchensink/2018/intro_django.rst
    :language: rst
    :end-before: A Video

As this document shows, you can also make an inline reference using Sphinx's
``ref`` directive.

If these ``category`` references point to an invalid value, Kaybee raises
an exception during execution.  Also, Kaybee keeps track of references,
allowing templates to list the references a document makes but also which
documents point to a reference.

The best part: defining your own vocabulary. Don't want ``category``? Make a
new scheme, such as ``author``.

Articles
========

The Kaybee core includes resources, widgets, references, Sphinx event
handlers, and more. It is useful for making a custom site or for writing a
basic site.

For most needs, you'll want a ready-to-go system that has made some decisions
for you. Kaybee's article plugins provide that:

- An ``article`` resource with richer metadata (appear in nav, published,
  etc.)

- A way to divide sites into "sections"

- A custom ``homepage`` resource

- Widgets that do certain kinds of listings, including overriding Sphinx's
  ``toctree``

- A ``category`` reference system

The article system also has a modern :ref:`category-kaybee_bulma` theme,
based on the :ref:`category-bulma` CSS framework, designed for use with it.
These docs use that theme.

Extensibility
=============

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
:ref:`category-bulma` with some interesting approaches. These docs
use the :ref:`category-kaybee_bulma`.

Additionally, Kaybee has a *lot* of unit tests (usually at or close to
100% coverage) and integration tests (usually over 90%.)