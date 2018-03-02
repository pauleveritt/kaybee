.. article::
    published: 2018-01-02 12:01

======
Events
======

Kaybee lets you register event handlers with directives, providing a
(hopefully) easier way to do work during the processing chain.

Sphinx Events
=============

Sphinx emits
:ref:`core events <sphinx:events>`
during the lifecycle of execution. These events cover the very first startup
of a builder, the reading of each document, the writing of each document, and
more.

Why does Kaybee have its own event system?

- Getting at Sphinx events requires an "extension" and a setup function to
  register events. Kaybee has a nicer system.

- No way to prioritize multiple callbacks for the same event, leading to
  long functions which violate single responsibility principle

- The arguments for the callbacks are baroque and missing higher-order stuff
  we might like. Stated differently, the surface area for those arguments is
  huge

- Sphinx event names are string-based, which are easy to get wrong, causing
  silent errors. Kaybee uses enums (and type hinting) to ensure accuracy.

- Test writing...meaning, controlling the API might make it easier to write
  isolated tests for isolated callbacks

The Dispatcher
==============

Kaybee's event system is actually pretty simple. For each Sphinx event, we
register a Kaybee function. This function looks in the (Dectate-based)
registry for callbacks interested in that event. Kaybee then "does something",
which might mean "massage the data needed for that event, sort the configured
callbacks based on a priority value, etc."

A Callback
==========

Let's say we want to do something before Sphinx starts reading documents.
It has an event ``env-before-read-docs`` for this. Here's and example of
registering an event:

.. code-block:: python

    from kaybee.plugins.events import SphinxEvent


    @kb.event(SphinxEvent.EBRD, 'coretype')
    def register_templates(kb, app, env, docnames):
        pass

That's all it takes. If the module that contains this gets imported by
anything, then this callback is registered.

Note the ``SphinxEvent.EPRD``. This is the enum which ensures the
proper event value.