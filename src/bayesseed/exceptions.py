"""Custom exceptions for Vestibular-BayesSeed."""


class BayesSeedError(Exception):
    """Base exception for package-specific errors."""


class ModuleLoadError(BayesSeedError):
    """Raised when a disease module cannot be loaded."""


class ModuleValidationError(BayesSeedError):
    """Raised when a disease module does not satisfy required structure."""


class InferenceError(BayesSeedError):
    """Raised when inference cannot be completed."""
