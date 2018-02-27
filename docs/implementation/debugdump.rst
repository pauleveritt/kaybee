.. article::
    published: 2018-01-02 12:01

.. _debugdump-implementation:

=========
Debugdump
=========

TDD with integration tests is a very productive way to add features and fix
bugs. However, writing assertions against HTML is a chore. Not only is it
clumsy to grab the node and value, but many times, the thing you're trying
to inspect isn't in the generated page.

The ``debugdump`` plugin addresses this by serializing "the system" to a
JSON file. You can then setup a ``sphinx.testing.fixture`` that reads the
JSON file into a Python object and makes it easily available in a test.
You're then working with data.

Let's look at the implementation of this plugin.

Discovery
=========

The plugin is in ``kaybee.plugins.debugdump.py``. Like other plugins, it
is imported via an ``importscan`` in ``kaybee.__init__.py``.

- datetime JSON handler

- Directive that allows plugins to register a dumper

- Dumper for kb itself

- Event for ECC that takes all of those top-level dumpers and writes to
  a file

- Integration test machinery to load a json_page

Then:

- Config knob to turn on/off