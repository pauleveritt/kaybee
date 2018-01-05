============
Generic Page
============


- By default, all pages that don't have a resource, get assigned a
  "genericpage" and stored in sphinx_app.genericpages

- The class used is kaybee.plugins.genericpage.genericpage.Genericpage

- By default, it uses a templatename of 'page.html' the Sphinx template

- You can change this in the resource YAML acquireds on the root, either
  with a ``template`` on ``genericpage`` or the ``all``

- Docs projects can register a different genericpage handler, to get a
  different set of decisions for template, or to have helper "view" methods

- Use ``kb.genericpage()`` to register your handler

- If you install a 3rd party plugin that installs a genericpage handler, use
  ``kb.genericpage(order=10)`` to give a higher priority...lowest "order"
  wins (default is 40)

- ``genericpage`` is put into html context, you can make your own class with
  helpers
