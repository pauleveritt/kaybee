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

Releases are driven by Travis. When a push is done with a tag, the Travis
build notices the tag and triggers the PyPI update. (Non-tagged pushes don't
trigger the PyPI part of ``.travis.yml``.)

#. Commit everything.

#. Bump the version using
   `bumpversion commands <https://github.com/peritus/bumpversion/issues/77#issuecomment-130696156>`_:

   - `bumpversion patch: 0.1.0 -> 0.1.1.dev0`

   - `bumpversion release: 0.1.1.dev0 -> 0.1.1`

   - `bumpversion minor: 0.1.1 -> 0.2.0.dev0`

   - `bumpversion dev: 0.2.0.dev0 -> 0.2.0.dev1`

   - `bumpversion release: 0.2.0.dev1 -> 0.2.0#. Tag the release.`

#. Commit, tag, push.

#. Run bumpversion to go back to dev

#. Run ``gitchangelog > CHANGES.md`` to generate the history that goes into
   the package. Tip: Use the commit message prefixes from their `reference
   <https://github.com/vaab/gitchangelog/blob/master/src/gitchangelog/gitchangelog.rc.reference>`_

#. Commit, push (so people can see the history.)