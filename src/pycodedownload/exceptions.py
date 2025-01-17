class ExtensionManagerError(Exception):
    """Base exception for the extension manager."""
    pass

class ConfigurationError(ExtensionManagerError):
    """Configuration related errors."""
    pass

class MarketplaceAPIError(ExtensionManagerError):
    """Marketplace API related errors."""
    pass

class DownloadError(ExtensionManagerError):
    """Download related errors."""
    pass
