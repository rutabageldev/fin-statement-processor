"""SecureVault encryption utilities using AES-256-GCM."""

import base64
import hashlib
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .exceptions import MasterKeyError
from .exceptions import SecretEncryptionError


class SecureVaultEncryption:
    """AES-256-GCM encryption for SecureVault secrets."""

    def __init__(self, master_key: str) -> None:
        """Initialize encryption with master key.

        Args:
            master_key: Base master key string from environment

        Raises:
            MasterKeyError: If master key is invalid
        """
        if not master_key:
            msg = "Master key cannot be empty"
            raise MasterKeyError(msg)

        min_key_length = 32  # Minimum key length for AES-256
        if len(master_key) < min_key_length:
            msg = "Master key must be at least 32 characters long"
            raise MasterKeyError(msg)

        self._master_key = master_key

    def _derive_key(self, salt: bytes) -> bytes:
        """Derive AES-256 key from master key using PBKDF2.

        Args:
            salt: Random salt for key derivation

        Returns:
            32-byte AES-256 key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bits
            salt=salt,
            iterations=100000,  # OWASP recommended minimum
        )
        return kdf.derive(self._master_key.encode("utf-8"))

    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext secret using AES-256-GCM.

        Args:
            plaintext: Secret value to encrypt

        Returns:
            Base64 encoded encrypted data: salt(32) + nonce(12) + ciphertext + tag(16)

        Raises:
            SecretEncryptionError: If encryption fails
        """
        try:
            # Generate random salt and nonce
            salt = os.urandom(32)  # 256-bit salt
            nonce = os.urandom(12)  # 96-bit nonce for GCM

            # Derive encryption key
            key = self._derive_key(salt)

            # Encrypt using AES-256-GCM
            aesgcm = AESGCM(key)
            ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)

            # Combine salt + nonce + ciphertext (includes tag)
            encrypted_data = salt + nonce + ciphertext

            # Return base64 encoded
            return base64.b64encode(encrypted_data).decode("ascii")

        except Exception as e:
            msg = f"Encryption failed: {e}"
            raise SecretEncryptionError(msg) from e

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt AES-256-GCM encrypted secret.

        Args:
            encrypted_data: Base64 encoded encrypted data

        Returns:
            Decrypted plaintext secret

        Raises:
            SecretEncryptionError: If decryption fails
        """
        try:
            # Decode base64
            data = base64.b64decode(encrypted_data.encode("ascii"))

            # Extract components
            salt = data[:32]  # First 32 bytes
            nonce = data[32:44]  # Next 12 bytes
            ciphertext = data[44:]  # Remaining bytes (ciphertext + tag)

            # Derive decryption key
            key = self._derive_key(salt)

            # Decrypt using AES-256-GCM
            aesgcm = AESGCM(key)
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)

            return plaintext.decode("utf-8")

        except Exception as e:
            msg = f"Decryption failed: {e}"
            raise SecretEncryptionError(msg) from e

    def verify_master_key(self, test_ciphertext: str) -> bool:
        """Verify master key by attempting decryption.

        Args:
            test_ciphertext: Known encrypted value to test against

        Returns:
            True if master key is correct, False otherwise
        """
        try:
            self.decrypt(test_ciphertext)
        except SecretEncryptionError:
            return False
        else:
            return True

    @staticmethod
    def generate_master_key() -> str:
        """Generate a cryptographically secure master key.

        Returns:
            64-character hex string suitable for use as master key
        """
        return os.urandom(32).hex()  # 256-bit key as hex string

    def get_key_fingerprint(self) -> str:
        """Get a fingerprint of the master key for verification.

        Returns:
            SHA-256 hash of master key (first 16 chars)
        """
        return hashlib.sha256(self._master_key.encode("utf-8")).hexdigest()[:16]
