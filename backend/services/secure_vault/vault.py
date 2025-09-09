"""SecureVault core service for secret management."""

import os
from datetime import UTC
from datetime import datetime

# Use dynamic imports to avoid circular dependencies
from typing import TYPE_CHECKING
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


if TYPE_CHECKING:
    from database import async_session_maker
    from models.orm import Secret
    from models.orm import SecretAuditLog
else:
    # Runtime imports for functions that need them
    from database import async_session_maker
    from models.orm import Secret
    from models.orm import SecretAuditLog
from .encryption import SecureVaultEncryption
from .exceptions import MasterKeyError
from .exceptions import SecretNotFoundError
from .exceptions import SecretValidationError


class SecureVault:
    """Core SecureVault service for encrypted secret management."""

    def __init__(self, master_key: str | None = None) -> None:
        """Initialize SecureVault with master key.

        Args:
            master_key: Master encryption key (defaults to SECURE_VAULT_MASTER_KEY env var)

        Raises:
            MasterKeyError: If master key is not provided or invalid
        """
        # Get master key from parameter or environment
        key = master_key or os.getenv("SECURE_VAULT_MASTER_KEY")
        if not key:
            msg = "Master key not provided. Set SECURE_VAULT_MASTER_KEY environment variable."
            raise MasterKeyError(msg)

        self.encryption = SecureVaultEncryption(key)
        self._key_fingerprint = self.encryption.get_key_fingerprint()

    async def store_secret(
        self,
        name: str,
        value: str,
        description: str | None = None,
        rotation_policy: dict[str, Any] | None = None,
        user_id: UUID | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> "Secret":
        """Store an encrypted secret.

        Args:
            name: Unique secret name/key
            value: Secret value to encrypt and store
            description: Human-readable description
            rotation_policy: JSON policy for automatic rotation
            user_id: User performing the operation
            ip_address: Request IP address for audit
            user_agent: Request user agent for audit

        Returns:
            Created Secret model

        Raises:
            SecretValidationError: If secret name already exists or validation fails
            SecretEncryptionError: If encryption fails
        """
        if not name or not name.strip():
            msg = "Secret name cannot be empty"
            raise SecretValidationError(msg)

        if not value:
            msg = "Secret value cannot be empty"
            raise SecretValidationError(msg)

        # Use imported models and session maker

        # Encrypt the secret value
        encrypted_value = self.encryption.encrypt(value)

        # Create secret record
        secret = Secret(
            name=name.strip(),
            encrypted_value=encrypted_value,
            description=description,
            rotation_policy=rotation_policy,
            access_count=0,
            key_fingerprint=self._key_fingerprint,
        )

        async with async_session_maker() as session:
            try:
                # Check if secret already exists
                existing = await session.execute(
                    select(Secret).where(Secret.name == name.strip())
                )
                if existing.scalar_one_or_none():
                    msg = f"Secret '{name}' already exists"
                    raise SecretValidationError(msg)

                # Store secret
                session.add(secret)
                await session.commit()
                await session.refresh(secret)

                # Log the operation
                await self._log_audit(
                    session=session,
                    secret_name=name.strip(),
                    action="WRITE",
                    user_id=user_id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details={
                        "description": description,
                        "has_rotation_policy": bool(rotation_policy),
                    },
                )

            except IntegrityError as e:
                await session.rollback()
                msg = f"Secret '{name}' already exists"
                raise SecretValidationError(msg) from e
            else:
                return secret

    async def retrieve_secret(
        self,
        name: str,
        user_id: UUID | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> str:
        """Retrieve and decrypt a secret value.

        Args:
            name: Secret name to retrieve
            user_id: User performing the operation
            ip_address: Request IP address for audit
            user_agent: Request user agent for audit

        Returns:
            Decrypted secret value

        Raises:
            SecretNotFoundError: If secret doesn't exist
            SecretEncryptionError: If decryption fails
        """
        # Use imported models and session maker

        async with async_session_maker() as session:
            # Find secret
            result = await session.execute(
                select(Secret).where(Secret.name == name.strip())
            )
            secret = result.scalar_one_or_none()

            if not secret:
                # Log failed access attempt
                await self._log_audit(
                    session=session,
                    secret_name=name.strip(),
                    action="READ",
                    user_id=user_id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details={"error": "Secret not found"},
                )
                msg = f"Secret '{name}' not found"
                raise SecretNotFoundError(msg)

            # Decrypt secret value
            decrypted_value = self.encryption.decrypt(secret.encrypted_value)

            # Update access tracking
            secret.access_count += 1
            secret.last_accessed_at = datetime.now(UTC)

            # Log successful access
            await self._log_audit(
                session=session,
                secret_name=name.strip(),
                action="READ",
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                details={"access_count": secret.access_count},
            )

            await session.commit()

            return decrypted_value

    async def update_secret(
        self,
        name: str,
        new_value: str,
        description: str | None = None,
        rotation_policy: dict[str, Any] | None = None,
        user_id: UUID | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> "Secret":
        """Update an existing secret value.

        Args:
            name: Secret name to update
            new_value: New secret value to encrypt and store
            description: Updated description (optional)
            rotation_policy: Updated rotation policy (optional)
            user_id: User performing the operation
            ip_address: Request IP address for audit
            user_agent: Request user agent for audit

        Returns:
            Updated Secret model

        Raises:
            SecretNotFoundError: If secret doesn't exist
            SecretValidationError: If validation fails
            SecretEncryptionError: If encryption fails
        """
        if not new_value:
            msg = "Secret value cannot be empty"
            raise SecretValidationError(msg)

        # Use imported models and session maker

        async with async_session_maker() as session:
            # Find existing secret
            result = await session.execute(
                select(Secret).where(Secret.name == name.strip())
            )
            secret = result.scalar_one_or_none()

            if not secret:
                msg = f"Secret '{name}' not found"
                raise SecretNotFoundError(msg)

            # Encrypt new value
            encrypted_value = self.encryption.encrypt(new_value)

            # Update secret
            secret.encrypted_value = encrypted_value
            secret.key_fingerprint = self._key_fingerprint

            if description is not None:
                secret.description = description
            if rotation_policy is not None:
                secret.rotation_policy = rotation_policy

            # Log the operation
            await self._log_audit(
                session=session,
                secret_name=name.strip(),
                action="WRITE",
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                details={
                    "operation": "update",
                    "description_updated": description is not None,
                    "rotation_policy_updated": rotation_policy is not None,
                },
            )

            await session.commit()
            await session.refresh(secret)

            return secret

    async def delete_secret(
        self,
        name: str,
        user_id: UUID | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> None:
        """Delete a secret permanently.

        Args:
            name: Secret name to delete
            user_id: User performing the operation
            ip_address: Request IP address for audit
            user_agent: Request user agent for audit

        Raises:
            SecretNotFoundError: If secret doesn't exist
        """
        async with async_session_maker() as session:
            # Find existing secret
            result = await session.execute(
                select(Secret).where(Secret.name == name.strip())
            )
            secret = result.scalar_one_or_none()

            if not secret:
                msg = f"Secret '{name}' not found"
                raise SecretNotFoundError(msg)

            # Log deletion before removing
            await self._log_audit(
                session=session,
                secret_name=name.strip(),
                action="DELETE",
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                details={
                    "secret_id": str(secret.id),
                    "access_count": secret.access_count,
                    "created_at": secret.created_at.isoformat(),
                },
            )

            # Delete secret
            await session.delete(secret)
            await session.commit()

    async def list_secrets(
        self,
        *,
        include_metadata: bool = False,
        user_id: UUID | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> list[dict[str, str | int | bool | None]]:
        """List all secrets with optional metadata.

        Args:
            include_metadata: Include access counts, timestamps, etc.
            user_id: User performing the operation
            ip_address: Request IP address for audit
            user_agent: Request user agent for audit

        Returns:
            List of secret information (without encrypted values)
        """
        async with async_session_maker() as session:
            result = await session.execute(select(Secret))
            secrets = result.scalars().all()

            # Log list operation
            await self._log_audit(
                session=session,
                secret_name="*",  # Special name for bulk operations  # pragma: allowlist secret # nosec B106 # noqa: S106
                action="READ",
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                details={
                    "operation": "list",
                    "count": len(secrets),
                    "include_metadata": include_metadata,
                },
            )

            secret_list: list[dict[str, str | int | bool | None]] = []
            for secret in secrets:
                secret_info: dict[str, str | int | bool | None] = {
                    "name": secret.name,
                    "description": secret.description,
                    "created_at": secret.created_at.isoformat(),
                    "updated_at": secret.updated_at.isoformat(),
                }

                if include_metadata:
                    secret_info.update(
                        {
                            "access_count": secret.access_count,
                            "last_accessed_at": secret.last_accessed_at.isoformat()
                            if secret.last_accessed_at
                            else None,
                            "key_fingerprint": secret.key_fingerprint,
                            "has_rotation_policy": bool(secret.rotation_policy),
                        }
                    )

                secret_list.append(secret_info)

            await session.commit()
            return secret_list

    async def rotate_secret(
        self,
        name: str,
        new_value: str,
        user_id: UUID | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> "Secret":
        """Rotate a secret with audit logging.

        Args:
            name: Secret name to rotate
            new_value: New secret value
            user_id: User performing the operation
            ip_address: Request IP address for audit
            user_agent: Request user agent for audit

        Returns:
            Updated Secret model

        Raises:
            SecretNotFoundError: If secret doesn't exist
            SecretValidationError: If validation fails
        """
        async with async_session_maker() as session:
            # Find existing secret
            result = await session.execute(
                select(Secret).where(Secret.name == name.strip())
            )
            secret = result.scalar_one_or_none()

            if not secret:
                msg = f"Secret '{name}' not found"
                raise SecretNotFoundError(msg)

            # Encrypt new value
            encrypted_value = self.encryption.encrypt(new_value)

            # Update secret
            old_fingerprint = secret.key_fingerprint
            secret.encrypted_value = encrypted_value
            secret.key_fingerprint = self._key_fingerprint

            # Log rotation
            await self._log_audit(
                session=session,
                secret_name=name.strip(),
                action="ROTATE",
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                details={
                    "old_key_fingerprint": old_fingerprint,
                    "new_key_fingerprint": self._key_fingerprint,
                    "access_count": secret.access_count,
                },
            )

            await session.commit()
            await session.refresh(secret)

            return secret

    async def get_audit_logs(
        self,
        secret_name: str | None = None,
        action: str | None = None,
        limit: int = 100,
    ) -> list["SecretAuditLog"]:
        """Retrieve audit logs for secret operations.

        Args:
            secret_name: Filter by specific secret name (optional)
            action: Filter by action type (optional)
            limit: Maximum number of records to return

        Returns:
            List of audit log entries
        """
        async with async_session_maker() as session:
            query = select(SecretAuditLog).order_by(SecretAuditLog.timestamp.desc())

            if secret_name:
                query = query.where(SecretAuditLog.secret_name == secret_name)
            if action:
                query = query.where(SecretAuditLog.action == action)

            query = query.limit(limit)

            result = await session.execute(query)
            return list(result.scalars().all())

    async def _log_audit(
        self,
        session: AsyncSession,
        secret_name: str,
        action: str,
        user_id: UUID | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Log secret operation for audit trail.

        Args:
            session: Database session
            secret_name: Name of secret involved
            action: Action performed (READ, WRITE, ROTATE, DELETE)
            user_id: User who performed the action
            ip_address: IP address of request
            user_agent: User agent string
            details: Additional context information
        """
        audit_log = SecretAuditLog(
            secret_name=secret_name,
            action=action,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.now(UTC),
            details=details,
        )

        session.add(audit_log)
        # Note: commit is handled by caller
