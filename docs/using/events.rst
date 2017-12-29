===========================
Registering Event Callbacks
===========================

Sphinx has a system for registering functions that can be run at different
times during the lifecycle of page building. This event system, though, is a
bit cryptic to use.

Kaybee provides an alternate event system. When Sphinx fires an event, Kaybee
looks in its registry for all the callbacks, and processes those callbacks in
a richer way. These callbacks are registered with directives.

Let's take a look.

Multiple Events and Ordering
============================

system_order vs. order

numbering