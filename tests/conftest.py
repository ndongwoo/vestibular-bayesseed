"""Pytest fixtures for Vestibular-BayesSeed.

These tests are intended to be copied into the repository root and run with:

    pytest

The fixtures add ``src/`` to ``sys.path`` so the tests can run from a source
checkout before the package is installed.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
DEFAULT_MODULES_DIR = PROJECT_ROOT / "default_modules"
EXAMPLES_DIR = PROJECT_ROOT / "examples"

if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


@pytest.fixture(scope="session")
def project_root() -> Path:
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def default_modules_dir() -> Path:
    assert DEFAULT_MODULES_DIR.exists(), "default_modules/ directory is required for tests."
    return DEFAULT_MODULES_DIR


@pytest.fixture(scope="session")
def examples_dir() -> Path:
    assert EXAMPLES_DIR.exists(), "examples/ directory is required for tests."
    return EXAMPLES_DIR


@pytest.fixture(scope="session")
def bppv_module_path(default_modules_dir: Path) -> Path:
    return default_modules_dir / "bppv.json"


@pytest.fixture(scope="session")
def md_module_path(default_modules_dir: Path) -> Path:
    return default_modules_dir / "meniere_disease.json"


@pytest.fixture(scope="session")
def pvp_bvp_module_path(default_modules_dir: Path) -> Path:
    return default_modules_dir / "pvp_bvp.json"
