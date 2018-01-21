=======
Layouts
=======

As explained in :doc:`../using/layouts`, Kaybee augments Sphinx themes with a
superset called *layouts*. This document describes the implementation.

Config
======

- Your ``conf.py`` file chooses and configures a Kaybee layout and a
  Sphinx theme in one shot:

  .. code-block:: python

        from mytheme import MyLayout

        html_theme = MyLayout(
            copyright='2001 A Space Odyssey',
            logo=dict(
                alt='My Logo',
                url='http://something'
                )
        )

- The layout class has a string representation which matches the layout
  "name" (see below)

- The values passed to the constructor go to pydantic model, which validates
  them against PEP 484 stuff

- The constructor then stores the validated values onto a ``props`` attribute

Layout Class
============

- The class is registered as a layout with a name

    .. code-block:: python

            from kaybee.plugins.layouts.base_layout import BaseLayout

            class Logo(BaseModel):
                img_url: str = None
                img_file: str = None
                alt: str = None

            @kb.layout('mylayout')
            class MyLayout(BaseLayout):
                copyright = 'All Rights Reserved'
                logo: Logo = None

- The package has a ``templates`` subdirectory and a ``static`` subdirectory,
  just like Sphinx themes

Registration
============

- When this is imported, Kaybee adds this layout to kb.config.layouts

- It's a conflict error if two classes register with the same name

Handlers
========

- A builder-init (or similarly early) handler finds the registered layout
  class and puts an instance onto ``sphinx_app``

- A handler for html page context injects the configured layout instance into
  the template

- A handler that registers the template directory

- A dumper that puts stuff into debugdump.json

Future Work
===========

Switchable Templates
--------------------

- We want to let resources specify (either directly or via acquireds) a
  different layout template to use.

- A resource's template would start with:

    .. code-block:: jinja

        {% extends resource.layout %}

- This would be a ``@property`` which returns the string of the template
  filename to use

- It *could* also choose an actually differently-registered layout, but that
  seems way overkill

- The class default ``@property`` could look first in the local YAML, then in
  acquireds, the perhaps a class name, before returning the default
  ``layout.html``

- Really ambitious resources could override this and provide logic that
  chose the layout template using other information/policies
