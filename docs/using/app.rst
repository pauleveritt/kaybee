===================
kb, the Default App
===================

Kaybee has a registry. The registry lets you add configuration statements
that form a plugin system.

What is this "registry"? Let's take a quick look.

Dectate and "apps"
==================

When you use a Kaybee directive such as
``@kb.resource('article')``, you are adding a configuration statement: "I
am adding a new kind of resource called ``article`` to the registry."

Dectate, the underlying configuration framework used by Kaybee, then springs
into action. ``resource`` is an "action" in Dectate terms. Something has
defined "resource" as a part of the registry that can accept configuration
statements conforming to some rules it defines.

But what is ``kb``? The various actions are grouped together into what Dectate
calls an "app class", or app. The app is the registry. Each action is a
class attribute. Every time you use the decorator, you add stuff to the
configuration via the action.

This app class -- such as ``kb`` -- isn't something you make an instance of.
Behind the scenes, weird stuff is happening with state being stored on the
class itself. This lets you simply import the app and do things, rather than
pass around a variable.

The ``kb`` App
==============

By default, Kaybee has one of these app classes called ``kb``. You can import
it in your documentation project and get going. It has some actions configured
alread: ``kb.event``, ``kb.resource``, ``kb.widget``, etc.

That's not your only choice, though.

Adding New Actions
==================

Kaybee is plugin-oriented. You might find some other plugin that does
something interesting. It needs to be added to your app class. Simply
subclass ``kb`` and add the actions you're interested in.

.. note::

    This section is fishy. Sure would be nice to figure out a way to
    just add plugins to the app.

Other Kinds of State
====================

As a closing point, we discussed how Dectate stores state on the class,
which means you don't have to pass around a registry. Just import it and you
get all the configuration added by any of the code.

Sure would be a great place to store document state, instead of passing around
a "site". At the moment, Kaybee doesn't plan to go that far.