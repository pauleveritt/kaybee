kaybee Static Sites for Knowledge Bases
=======================================


Development
-----------

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