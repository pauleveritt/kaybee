# Simplest test possible, is the package importable


def test_import():
    from kaybee import __version__
    assert isinstance(__version__, str)
