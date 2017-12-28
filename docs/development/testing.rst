=======
Testing
=======

Kaybee aims to be developed using TDD. This isn't always easy with Sphinx. As
such, the test strategies for unit testing and integration testing vary.

Both types of tests use ``pytest`` as the foundation, with top-level
``conftest.py`` fixtures providing variations of important common data and
mocks.

Unit Testing
============

The unit tests under ``tests/unit`` attempt to provide decent coverage for
features and aspects of the system. Sphinx makes it hard to test, as it has
deeply-nested data passed as arguments into functions. Kaybee itself has been
designed to isolate its feature implementations from the Sphinx environment,
to make testing easier.

Integration Testing
===================

These tests are much slower but enable very detailed, feature-oriented
coverage.

The tests are under ``tests/integration``. The ``conftest.py`` fixtures file
has an important series of setup function which tap into pytest-oriented
fixtures provided by Sphinx. These make it convenient to setup and tear down
the isolated running of ``sphinx-build`` in a tmp directory.

Each of the features are then in separate test files.

The fixtures provide two variations of results:

- HTML pages wrapped in beautifulsoup to allow path-oriented testing of markup

- JSON "pages" parsed into Python dicts to reason about the results as data

