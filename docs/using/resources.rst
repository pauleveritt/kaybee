=========
Resources
=========

Resources are the heart of Kaybee. They allow a Sphinx page to become a unit
of knowledge which can be listed, queried, and referenced. You simply embed
some YAML into a document to turn it into a resource. If you provide a bad
value, an associated schema will tell you.

You can use the built-in resource, make your own kinds of resources, or use
Kaybee plugins such as ``articles`` that provide ready-to-go systems of
resource types and related parts such as widgets.

Quick Tutorial
==============

Let's say I had a Sphinx page such as the root of a docs project:

.. code-block:: rst

    Hello World
    ===========

What does it take to turn this document into a "resource"? Kaybee ships
with a Sphinx direct ``resource`` which you can use:

.. code-block:: rst

    .. resource::

    Hello World
    ===========

I have now turned this document into a "resource" of resource type "resource".
The page now renders in Sphinx slightly differently: it is using the Jinja2
template associated with that resource type, instead of Sphinx's
``page.html``. More on both of these points to follow.

Let's say, for this particular document, I want a different template. Here
comes the YAML:

.. code-block:: rst

    .. resource::
        template: mypage

    Hello World
    ===========

Kaybee will now look for a Jinja2 template named ``mypage.html`` in one of
Sphinx's registered directories. You now create ``_templates/mypage.html``
in your Sphinx docs project, beside the ``conf.py``.

The indented content under ``.. resource::`` (the directive "content") is
actually interpreted as YAML. Which is typed, so an integer is different than
a string. Kaybee validates the YAML against a schema. Let's see that in action
by changing the template value to a number:

.. code-block:: rst

    .. resource::
        template: 999

    Hello World
    ===========

When you run Sphinx, Kaybee throws a validation error because template is
expected to be a string.

Kaybee's ``resource`` resource type is very basic. Its purpose is to provide
a minimal building block for richer resource types, such as
``kaybee.plugins.articles`` or ones that you make. That's the topic of the
:doc:`../extending/index` section, but as a sneak peek, here's where Kaybee
declares the ``resource`` directive and resource type:

.. literalinclude:: ../../kaybee/plugins/resources/resource.py

Let's talk a little more about what is happening when you use this resource.

Base Resource
=============

The base resource, available in RST with ``.. resource::`` and in Python as a
base class, represents the basic building block of a unit of information in
Kaybee. Add a little bit of YAML to your document and things spring into
action:

- Embedding some (schema validated) data available as ``props``

- Controlling the template used to render

- Assembling a hierarchy of parents

- Rendering information to JSON, e.g. for use in the debugdumper

- Adding an instance of that resource to a "database" hanging off the
  Sphinx app

- Making the resource instance available in the Jinja2 template

Let's go through the basics.

The Base Directive
------------------

Sphinx (actually reStructuredText) has a concept of
:ref:`directives <sphinx:directives>` -- sort of like tags in HTML. RST and
Sphinx have a bunch of directives built-in, but you can also register
your own directives.

That's what Kaybee does. You define "kinds of things" called *resource
types* and Kaybee generates directives which you can put in your document.
As a convenience, Kaybee has a ``resource`` directive -- a very simple,
minimal way to get started.

Sphinx directives have some information that goes inside of them. Kaybee
directives treat that information as YAML which gets validated against a
schema using a package called
`pydantic <https://pydantic-docs.helpmanual.io>`_. The result of this
validation is stored on the resource instance's ``props`` attribute.

The ``resource`` directive only has 2 things that can go in its YAML:

- ``template``, an optional string which chooses a template for *this*
  document

- ``acquireds``, which we talk about below under *Parents*

The Resource
------------

Every Sphinx page gets turned into a basic "resource", even if you don't put
the directive. Resource data is stored on the Sphinx ``app`` object, which
Kaybee makes available in templates under the ``sphinx_app`` variable and
passes in to Kaybee event handlers.

Kaybee adds a ``resources`` collection to the Sphinx app, where it stores
resources, using the document's ``docname`` as the key. For example, a Jinja2
template might grab a specific resource's title with following:

.. code-block:: jinja

    <div>{{ sphinx_app.resources['folder1/subfolder2/about'].title }}</div>

Kaybee also makes a variable ``resource`` available in Jinja2 templates, bound
to the resource for the current docname.

Parents
-------

Files on disk are organized into folders and subfolders. So are static
websites. And so is Sphinx, which has a
:ref:`sphinx:toctree directive <toctree-directive>` which lets a document
list (in order or wildcard) its children. As such, Sphinx has a very strong
concept of hierarchy in a document collection.

As you organize your ``.rst`` documents into folders and subfolders, you might
have reasons to look at your Kaybee resource's "parents". For example:

- Use templating to assemble breadcrumbs

- Divide your site into "sections" and show which section is active

- Do queries to find only resources in a certain section

- Avoid repetition by pushing some common properties or policies to parent
  folders' YAML

Kaybee keeps track of parents by storing the immediate-parent docname on each
resource, with the root being the first in the sequence. Thus, for a docname
of ``folder1/subfolder2/about``, the parents would be:

.. code-block:: python

    ['index', 'folder1/index', 'subfolder2/index']

The resource has a method ``parents`` which, when passed the resources
collection, will return the actual resource objects for each parent. This
can be used in templates.

Acquired Properties
-------------------

Sometimes you have properties that might appear in all, or some, documents
in part of your site. You'd prefer to define the property once, at the
top of that part of the tree, then have child nodes "acquire" them as
needed. Like inheritance, but for data instead of classes. And like
inheritance, a child can provide its own value instead of "acquiring" it
from its parentage.

This is particularly useful for system-oriented properties such as template
name. You might want all the templates for a certain part of the site to
be customized. Or you might want a custom template only for a certain
resource type.

Kaybee supports setting an ``acquired`` mapping value in the YAML of a node,
to provide property values for its ancestors. This mapping can provide
per-type mappings of properties or a mapping to apply to all types.

.. note::

    Regular properties have validated schemas. You can't just add an
    extra property. Acquired properties, though, allow anything inside
    their mappings -- the acquired property doesn't have to be in a schema.

Here's an example of a parent which takes control of different kinds of
children:

.. literalinclude:: ../../tests/integration/roots/test-acquire/folder1/index.rst

This document says that anything anywhere under ``folder`` can look up
certain prop values based on resource type (or ``all``, for props that
any resource type can acquire.)

It isn't just ``template``...any property can be "pushed up" to a parent,
grandparent, etc. But if one of the children defines that property locally,
it's used instead of the parent's property.


TODO
====

- Custom resource type, both in ``conf.py`` and in ``kaybee_plugins``
- Putting local definitions in a docs project dir NOT named ``kaybee_plugin``
- The current resource is available in templates as ``resource``
- genericpage
- Query.filter_collection
- Uses the rtype as the base name (without ``.html``) for the template