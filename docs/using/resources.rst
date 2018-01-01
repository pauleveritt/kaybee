=========
Resources
=========

Resources are the heart of Kaybee. They allow a Sphinx page to become a unit
of knowledge which can be listed, queried, and referenced. You simply embed
some YAML into a document to turn it into a resource. If you provide a bad
value, an associated schema will tell you.

You can use the built-in resource, make your own kinds of resources, or use
Kaybee extensions that provide ready-to-go systems of resource types and
related parts such as widgets.

Base Resource
=============

The base resource, available in RST with ``.. resource::`` and in Python as a
base class, represents the basic building block of a units of information in
Kaybee. Add a little bit of YAML to your document and things spring into
action:

- Controlling the template used to render

- Assembling a hierarchy of parents

- Rendering information to JSON, e.g. for use in the debugdumper

Let's go through the basics.

The Base Directive
------------------

- The Properties Model

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

    <div>{{ sphinx_app.resources['folder1/subfolder2/about'] }}</div>

Kaybee also makes a variable ``resource`` available in Jinja2 templates, bound
to the resource for the current docname.

Parents
-------

As you organize your ``.rst`` documents into folders and subfolders, you might
have reasons to look at your "parents". For example:

- Use templating to assemble breadcrumbs

- Divide your site into "sections" and show which section is active

- Avoid repetition by pushing some common properties or policies to parent
  folders' YAML

Kaybee keeps track of parents by storing the immediate-parent docname on each
resource, with the root being the first in the sequence. Thus, for a docname
of ``folder1/subfolder2/about``, the parents would be:

.. code-block:: python

    ['index', 'folder1/index', 'subfolder2/index']

The resource has a method ``parents`` which, when passed the resources
collection, will return the actual resource objects for each parent.

- ``.. resource::`` as a built-in resource type
- Custom resource type, both in ``conf.py`` and in ``kaybee_plugins``
- Putting local definitions in a docs project dir NOT named ``kaybee_plugin``
