========================
Kaybee Development Setup
========================

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

Release
-------

#. Bump the version using ``bumpversion``:

   - https://legacy-developer.atlassian.com/blog/2016/02/bumpversion-is-automation-for-semantic-versioning/

   - https://github.com/peritus/bumpversion/issues/77#issuecomment-130696156

#. Tag the release.

#. Run ``gitchangelog`` to generate the history that goes into the package.

#. Generate the package using ``python setup.py sdist bdist_wheel``

#. Upload to PyPI using ``twine``