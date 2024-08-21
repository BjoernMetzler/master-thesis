import pint

try:
    import importlib.resources as pkg_resources
except ImportError:
    # python < 3.7
    import importlib_resources as pkg_resources

import pkg_resources # type: ignore

unit = pint.UnitRegistry(system='mks')
# Assuming '__package__' is your current package name and "gaslib_units.txt" is the file in your package
unit.load_definitions(pkg_resources.resource_filename(__package__, "gaslib_units.txt"))
