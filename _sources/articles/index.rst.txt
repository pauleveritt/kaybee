.. section::
    style: primary
    in_nav: True
    nav_title: Articles
    weight: 25
    published: 2018-01-01 12:00
    acquireds:
        all:
            style: primary


==================
The Article System
==================

- 3 flavors for formatted dates, each overridable as a setting, usable
  as a Jinja2 filter

- Articles can be in a "series" which shows a block at the bottom. The
  parent should have ``is_series: True`` in the YAML.
