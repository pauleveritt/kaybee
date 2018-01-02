==========
Directives
==========

Here's how the ``resources`` plugin uses directives:

- On the ``env-before-read-docs`` event, scan the registry for defined
  resource types. Each of these needs a directive

- Call the Sphinx ``app.add_directive`` on each, creating a directive with
  the name of the resource type and a ResourceDirective class

