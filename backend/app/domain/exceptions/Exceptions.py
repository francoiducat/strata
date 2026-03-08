"""
Custom domain-specific exceptions.
"""

class AssetNotFound(Exception):
    """Raised when an asset is not found."""

class AssetTypeNotFound(Exception):
    """Raised when an asset type is not found."""

class PortfolioNotFound(Exception):
    """Raised when a portfolios is not found."""

class CategoryNotFound(Exception):
    """Raised when a category is not found."""
class TagNotFound(Exception):
    """Raised when a tag is not found."""

class DuplicateName(Exception):
    """Raised when a name violates a unique constraint (tags, categories)."""

class CategoryHasChildren(Exception):
    """Raised when attempting to delete a category that has child categories."""
