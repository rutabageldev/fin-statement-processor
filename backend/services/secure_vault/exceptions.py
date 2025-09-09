"""SecureVault exception classes."""


class SecureVaultError(Exception):
    """Base exception for SecureVault operations."""


class MasterKeyError(SecureVaultError):
    """Raised when there are issues with the master key."""


class SecretNotFoundError(SecureVaultError):
    """Raised when a requested secret is not found."""


class SecretEncryptionError(SecureVaultError):
    """Raised when encryption/decryption fails."""


class SecretValidationError(SecureVaultError):
    """Raised when secret validation fails."""
