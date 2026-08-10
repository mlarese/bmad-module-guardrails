from pathlib import Path

EXPORT_ROOT = Path("/srv/exports")


def read_export(filename: str) -> bytes:
    return (EXPORT_ROOT / filename).read_bytes()
