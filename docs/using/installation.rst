============
Installation
============

For now, Kaybee expects you to generate a Sphinx project, then edit the
*doc project* and its ``conf.py`` file.

Steps
=====

#. Use :doc:`sphinx-quickstart <sphinx:tutorial>` to generate a documentation
   project.

#. Install ``kaybee`` with ``pip install kaybee``

Setup
=====

Kaybee is added to your Sphinx project like any other Sphinx extension:

#. Edit ``docs/conf.py``

#. Add ``kaybee`` to the list of Sphinx extensions. You can do this as a
   string value. As a more reliable way, put Python's import facility to
   work to generate the string, to avoid typos:

Here's an example from a simple Kaybee integration test:

.. literalinclude:: ../../tests/integration/roots/test-setup/conf.py

Running
=======

Sphinx contains a command-runner to build your docs. For example, run the
following from the directory above your docs:

.. code-block:: bash

    $ sphinx-build -E -b html docs docs/_build

This will read docs in your ``docs`` directory and generate HTML output
in ``docs/_build``.

Alternatively you can use the :ref:`live reload <livereload_script>` script to
have docs automatically build with browser reload on changes.

.. note::

    Kaybee can't use Sphinx's incremental rebuild nor parallel read
    options. Make sure to run Sphinx with ``-E`` to rebuild on each run.

Sphinx Customization
====================

At this point you can customize Sphinx without writing Python. You can
make a ``_templates`` dire

Other Choices
=============

ablog, sphinxcontrib_needs, certain themes.