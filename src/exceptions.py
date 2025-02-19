from typing import Optional


class STPCliError(Exception):
    """Base exception for all STP CLI errors."""

    pass


class FileOperationError(STPCliError):
    """Raised when file operations fail."""

    def __init__(self, message: str, path: Optional[str] = None):
        self.path = path
        super().__init__(f"{message} Path: {path}" if path else message)


class ValidationError(STPCliError):
    """Raised when validation fails."""

    pass


class GeometryError(STPCliError):
    """Raised when geometry operations fail."""

    pass
