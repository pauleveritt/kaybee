.. article::
    published: 2018-01-02 12:01

==============
Setup Function
==============

Sphinx extensions are registered in a documentation project's ``conf.py``
file. What does this do? It finds a ``setup`` function in the package
added to the extensions sequence, then runs it, passing in the Sphinx
``app``. This is covered in the
:doc:`Sphinx extension guide <sphinx:extdev/appapi>`.

Like other Sphinx extensions, Kaybee keeps a minimal approach to the
``setup`` function. Most of the work is done by functions imported from
elsewhere. Kaybee's setup does the following:

- Add a config value, letting a "SiteConfig" be used in the ``conf.py``

- Registers a custom ``TemplateBridge``, to allow post-render handlers

- Connecting Kaybee's event system into the various Sphinx events

Here is Kaybee's ``setup`` function:

.. literalinclude:: ../../kaybee/__init__.py
