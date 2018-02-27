.. article::
    published: 2018-01-02 12:01

======
Models
======

Resources let authors embed properties onto a resource. The site settings let
users configure a docs project.

In both cases, the values provided are validated against a schema expressed
as a *model*. Kaybee uses the ``pydantic`` package to express schemas using
Python type hinting.

- Base models
- When does validation occur
- Validation errors
