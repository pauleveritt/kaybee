.. article::
    published: 2018-01-02 12:01

=========
Templates
=========

Local Templates
===============

You can override templates in a docs project. Simply put a ``_templates``
directory next to your ``conf.py`` file. Then put your templates in there.
This uses the normal Sphinx layered namespace approach to template location,
but templates in this directory override any with the same name in other
directories.

For example, ``_templates/layout.html`` will override the layout template.
``_templates/page.html`` overrides the template used for normal Sphinx pages.
After that, you can provide templates with filenames for your resource types,
or names manually provided in the YAML for a resource, widget, etc.