"""Load JSON disease modules and sensitivity configurations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .exceptions import ModuleLoadError
from .schema_validation import validate_module


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a JSON object from *path*."""
    p = Path(path)
    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:  # pragma: no cover - message wrapper
        raise ModuleLoadError(f"Could not load JSON from {p}: {exc}") from exc
    if not isinstance(data, dict):
        raise ModuleLoadError(f"JSON root must be an object: {p}")
    return data


def load_module(path: str | Path, *, validate: bool = True) -> dict[str, Any]:
    """Load one disease module from a JSON file."""
    module = load_json(path)
    if validate:
        validate_module(module)
    module.setdefault("_source_path", str(Path(path)))
    return module


def is_probable_module(data: dict[str, Any]) -> bool:
    """Return true if a JSON object looks like a disease module."""
    return all(k in data for k in ("module_id", "target_diseases", "edges"))


def load_modules(
    path: str | Path, *, validate: bool = True, strict: bool = False
) -> list[dict[str, Any]]:
    """Load disease modules from a file or directory.

    Non-module JSON files such as schemas or sensitivity configuration files are
    skipped by default when loading from a directory. Set ``strict=True`` to make
    any invalid JSON file raise an error.
    """
    p = Path(path)
    if p.is_file():
        return [load_module(p, validate=validate)]
    if not p.exists() or not p.is_dir():
        raise ModuleLoadError(f"Module path does not exist or is not a directory: {p}")

    modules: list[dict[str, Any]] = []
    for json_path in sorted(p.glob("*.json")):
        try:
            data = load_json(json_path)
            if not is_probable_module(data):
                if strict:
                    raise ModuleLoadError(f"JSON file does not look like a module: {json_path}")
                continue
            if validate:
                validate_module(data)
            data.setdefault("_source_path", str(json_path))
            modules.append(data)
        except Exception:
            if strict:
                raise
            continue
    if not modules:
        raise ModuleLoadError(f"No disease modules found in: {p}")
    return modules


def load_sensitivity_config(path: str | Path) -> list[dict[str, Any]]:
    """Load a sensitivity-ranges JSON file.

    The function accepts either the project format ``{"items": [...]}`` or a raw
    list of sensitivity items.
    """
    data = load_json(path)
    items = data.get("items", data)
    if not isinstance(items, list):
        raise ModuleLoadError("Sensitivity configuration must contain an 'items' list.")
    return [dict(item) for item in items]
