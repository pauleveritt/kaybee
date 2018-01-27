# Now

- Make a full-featured integration test for articles, then link to that 
  on the docs/index.rst (instead of inlining some possibly-broken stuff)
  
# Next

- GitHub deployment with doctr

- Get kaybee_settings into the html context as ``settings``

- Postrender (which skips widget rendering)

- XSLT builder

- Feeds

# Could Be Better

- Setting to turn on/off "is_published"

- "Layout" concept the unify theme with computation and settings, with 
  switchable templates (context, settings, etc.)

- Update documentation

    - Re-organizing "Using" to be plugin-based

- Purge resources events (but document that it probably won't be used)

- RST-rendered field type and excerpt

- Like ablog, get title in resources.events using node['title'] or 
  _get_section_title
  
- Make relative/absolute URLs work, e.g. /blog vs. Sphinx rendered with 
  "pathto" available in widgets
  
- Have a date format in config like ablog line 280 post.py

- A model with a ReferenceField doesn't fail when the value points at 
  a non-existent reference

- Figure out integration test for Sphinx raising exceptions (which will 
  allow big increase in integration test coverage)

- The OOTB references directive requires template: page

- Instead of handlers for every doc, that traverse the doctree...one custom 
  handler which does one traversal calls handlers (performance improvement)

- Resources: Allow resources to override the template directory registration 
  by making the function read a value returned from the resource type 
  class

- Feed publish dates with configurable timezones

- Redirects like ABlog

- Get LiveSearch box working

- Icon for LiveSearch box

