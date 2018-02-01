=======
Widgets
=======

Notes
=====

- Kaybee makes a new kind of directive for each registered (via decorator)
  widget.

- There is a single kind of distutils node "widget". Nodes are the things
  that get injected into the doctree. The various directives result in
  a single node which has the name of the directive as an attribute.

- Uses the wtype as the base name (without ``.html``) for the template