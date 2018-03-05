# Now

- Update documentation

    - Re-organizing "Using" to be plugin-based

# Next

- Search

- Images

- Overhaul acquire and template to have shared code which also eliminates 
  duplicating style in a section
  
- The OOTB references directive requires template: page

- Get rid of widget make_context and just have a standard for getting 
  results as a property (rather than doing it up front)

# Could Be Better

- Allow a reference hierarchy e.g. ``frontend-jest`` to let categories 
  be grouped in super-categories

- Feeds

- Get kaybee_settings into the html context as ``settings``

- Setting to turn on/off "is_published"

- Give everything in articles the hero treatment

- "Layout" concept the unify theme with computation and settings, with 
  switchable templates (context, settings, etc.)

- RST-rendered field type and excerpt

- Like ablog, get title in resources.events using node['title'] or 
  _get_section_title
  
- A model with a ReferenceField doesn't fail when the value points at 
  a non-existent reference

- Figure out integration test for Sphinx raising exceptions (which will 
  allow big increase in integration test coverage)

- Instead of handlers for every doc, that traverse the doctree...one custom 
  handler which does one traversal calls handlers (performance improvement)

- Resources: Allow resources to override the template directory registration 
  by making the function read a value returned from the resource type 
  class

- Feed publish dates with configurable timezones

- Redirects like ABlog


