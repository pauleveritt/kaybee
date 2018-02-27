.. article::
    published: 2018-01-02 12:01

=========
Resources
=========

The ``kaybee.plugins.resources`` plugin is the heart of Kaybee. It brings
provides base models, a ready-to-go resource, a database on the Sphinx app
object, and more.

Plugin Initialization
=====================

The plugin is read in ``kaybee.__init__.py``  when ``importscan.scan``
imports ``kaybee.plugins.events.py``. This module has event handlers to:

- Initialize the Sphinx ``app`` to hold a ``Resources`` instance

- ...and more

Resources Database
==================

``resources`` has an event handler that is run on the Sphinx
``builder-inited`` event. The handler makes an instance of ``Resources``
and adds it to the ``app`` object.

This ``Resources`` object is a Python dictionary (``UserDict``) which
overrides some of the built-in methods. For example, adding a resource does
several things behind the scenes:

Notes
=====

- Uses the rtype as the base name (without ``.html``) for the template

- Adding resource container to sphinx_app

- Adding sphinx app to html context

- Validation

- Getting the resource into the html context
