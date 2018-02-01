=======
Testing
=======

Kaybee aims to be developed using TDD. This isn't always easy with Sphinx. As
such, the test strategies for unit testing and integration testing vary.

Both types of tests use ``pytest`` as the foundation, with top-level
``conftest.py`` fixtures providing variations of important common data and
mocks.

Personal Preferences
====================

I spend most of my development time in TDD. It's more efficient than running
Sphinx and looking at a browser. I try to avoid taking a shortcut and running
Sphinx directly and checking the output. It's pretty easy to make a small
integration test.

For PyCharm, when I actually run Sphinx, I don't use the Sphinx-flavored run
configuration. I make a Pythonrun config that points at my
``sphinx-quickstart``, with arguments of ``-E -b html . _build``, and a
working directory above the ``docs`` directory.

Unit Testing
============

The unit tests under ``tests/unit`` attempt to provide decent coverage for
features and aspects of the system. Sphinx makes it hard to test, as it has
deeply-nested data passed as arguments into functions. Kaybee itself has been
designed to isolate its feature implementations from the Sphinx environment,
to make testing easier.

To make test-running faster (especially under the debugger), and to focus on
on the task at hand, right-click on the test/class/file/directory that you
want to run and choose ``Run 'py.test' on ...``. Or better yet, choose to
run that test using ``Debug 'py.test' on ...``. PyCharm creates a temporary
(gray colored name) run configuration on-the-fly and sets that as the active
run config.

To go into real TDD mode, using ``Run`` and click ``Toggle auto-test`` then
run. PyCharm will re-run your selected test/tests as you type your code. The
delay is configurable.

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

The Kaybee integration tests favor the latter. Read more about this in
:ref:`debugdump-dev`. For example, here is a simple example of a debugdump
test:

.. literalinclude:: ../../tests/integration/test_debugdumper.py

The top-level ``conftest.py`` has the magic from ``sphinx.testing.fixtures``
that makes this work, along with a customization that does cleanup of the
Sphinx build at the appropriate time.