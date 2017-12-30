=========
Debugging
=========

Most of your Kaybee development will involve making mistakes.
Which means most of your time is spent debugging.

.. _debugdump-dev:

Debugdump
=========

It can be hard to find out what's going on with your Kaybee configuration and
state. What is the ``published`` value on a certain resource? Unit testing
isn't always the right fit, running Sphinx and guessing at the output is
frustrating, and making an integration test helps but you have to look at
the HTML rendering.

Or do you? The ``debugdump`` plugin serializes a JSON representation of your
entire system, into a single file. When combined with JSON-oriented
integration tests, this is a key tool during development.

To use it, write some code like this:

.. code-block:: python

    @kb_app.dumper('resources')
    def handle_event(kb_app=None):
        return dict(
            resource=dict(
                published=datetime.datetime.now()

            )
        )

The dict you return will be merged with the dicts from all the other
callbacks and written to ``debug_dump.json`` in the output directory. You
can then write integration test fixtures which load this file, letting you
easily make assertions about the state of the system.

For more information, read about the
:ref:`implementation of debugdump <debugdump-implementation>`.

Use the Debugger
================

PyCharm's debugger is very fast, especially for Python 3.6+ projects (and
Kaybee requires Python 3.6+). Most of the time I just run under the debugger.
I can then set a breakpoint and look at stuff without the context switch of
changing "modes".

As a note, when running tests under the debugger, the nice graphical test
window is under the "Console" tab. You can get to the console prompt, but due
to a bug, it doesn't show output. You're better off using PyCharm's graphical
``Evaluate Expression`` tool.

When you're at a breakpoint in PyCharm, remember that you can quickly spot
variable values with the psuedo-comments PyCharm inserts in your code.

When running your integration tests, remember to use the debugger there as
well, as it is a very productive mode to figure out what's going on.
