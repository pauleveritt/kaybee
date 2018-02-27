.. article::
    published: 2018-01-02 12:01

=================
Development Setup
=================

Want to hack on Kaybee? This page gives instructions for getting an
environment setup, as well as making releases.

Development
-----------

You'll want a
:ref:`virtual environment <python:tut-venv>`
with an "editable" project.

#. Make a virtualenv e.g. ``python3 -m venv env36``

#. Update pip stuff with ``pip install --upgrade pip setuptools wheel``

#. ``pip install -r requirements.txt`` to get dev requirements plus the
   editable package.

.. _livereload_script:

Live Reload
-----------

It's a chore to fire up a web server, make a change to your docs/code, re-run
Sphinx, possibly re-run Webpack, and then reload your browser. With help
from `livereload <https://pypi.python.org/pypi/livereload>`_ this can be made
easier. It watches for changes, runs some commands, and tells the browser
to reload.

You can run this with defaults with the following:

.. code-block:: bash

    $ python -m kaybee.utils.livereload

This will watch for any changes in the ``kaybee`` or ``docs`` directory,
minus any changes in ``_build``, and re-run Sphinx. You can subclass
``Livereload`` to change some options.

Release
-------

#. Bump the version using ``bumpversion``:

   - https://legacy-developer.atlassian.com/blog/2016/02/bumpversion-is-automation-for-semantic-versioning/

   - https://github.com/peritus/bumpversion/issues/77#issuecomment-130696156

#. Tag the release.

#. Run ``gitchangelog`` to generate the history that goes into the package.
   Tip: Use the commit message prefixes from their `reference
   <https://github.com/vaab/gitchangelog/blob/master/src/gitchangelog/gitchangelog.rc.reference>`_

#. Generate the package using ``python setup.py sdist bdist_wheel``

#. Upload to PyPI using ``twine``