"""Vestibular-BayesSeed core package.

A small, reusable engine for JSON-defined, evidence-anchored logistic Bayesian
network modules. The package is intended for research and educational use only;
it is not a validated clinical decision-support system.
"""

from .inference import infer_case, infer_module, infer_modules
from .logistic_cpd import logit, sigmoid, logistic_probability
from .module_loader import load_module, load_modules
from .schema_validation import validate_module

__all__ = [
    "infer_case",
    "infer_module",
    "infer_modules",
    "logit",
    "sigmoid",
    "logistic_probability",
    "load_module",
    "load_modules",
    "validate_module",
]

__version__ = "0.1.0"
