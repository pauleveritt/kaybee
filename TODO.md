# Now

- Move excerpt support to article

# Next

- Get kaybee_settings into the html context as ``settings``

- toctree handling in pbr.widgets.events.py (had to be in the core before)


# Could Be Better

- "Layout" concept the unify theme with computation and settings, with 
  switchable templates (context, settings, etc.)

- Purge resources events (but document that it probably won't be used)

- Write integration test for resource returning test.html

- Figure out integration test for Sphinx raising exceptions (which will 
  allow big increase in integration test coverage)

- The OOTB references directive requires template: page

- Instead of handlers for every doc, that traverse the doctree...one custom 
  handler which does one traversal calls handlers (performance improvement)

- Integration bumpcoverage

- Update documentation

    - Re-organizing "Using" to be plugin-based

- Resources: Allow resources to override the template directory registration 
  by making the function read a value returned from the resource type 
  class
  
- Resources: kbtype -> rtype

- Overridable toctree with a configuration knob to turn it on