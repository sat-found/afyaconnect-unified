"""Pytest availability marker for integration (server-backed tests skip without Tryton)."""
import shutil

collect_ignore = []
HAS_TRYTON = shutil.which('trytond-admin') is not None  # noqa: F841
