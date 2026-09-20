"""Services that orchestrate adapters through Protocols (`PLAN.md` §2.2).

A service never imports `storage`, `sources` or `providers`: it declares the shape it needs
as a Protocol here and `cli` injects the concrete instance. That is what keeps `core`
free of adapter dependencies while still owning the behaviour.
"""
