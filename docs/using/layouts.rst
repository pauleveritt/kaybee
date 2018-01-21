=======
Layouts
=======

Sphinx has a concept of :doc:`themes <sphinx:theming>` which "controls
HTML output" by collecting templates, stylesheets, and static files. This
works well: you can make your own local theme or make a Python package
which contains all the assets. Sphinx themes have a somewhat-rich system of
theme options which can be set in the Sphinx config file.

Kaybee introduces a superset of Sphinx themes called *layouts*. A Kaybee
layout is a Sphinx theme which adds the following:

- An instance of a layout class is added to the template environment. This
  lets you put logic and configuration needed for global rendering, in one
  place.

- Instead of Sphinx's system of theme options, use the pydantic system of
  PEP-484 validated models that resources uses

This foundation paves the way to later have switchable layouts. Meaning, some
pages use the main master template, other use a different one.
