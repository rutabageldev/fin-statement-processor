"""Admin API endpoints for SecureVault secret management."""

from typing import Any
from typing import cast
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from pydantic import BaseModel
from pydantic import Field

from services.secure_vault import MasterKeyError
from services.secure_vault import SecretEncryptionError
from services.secure_vault import SecretNotFoundError
from services.secure_vault import SecretValidationError
from services.secure_vault import SecureVault


router = APIRouter(prefix="/admin/secrets", tags=["Admin - Secrets"])


# Request/Response models
class SecretCreateRequest(BaseModel):
    """Request model for creating a new secret."""

    name: str = Field(
        ..., min_length=1, max_length=255, description="Unique secret name"
    )
    value: str = Field(..., min_length=1, description="Secret value to encrypt")
    description: str | None = Field(None, description="Human-readable description")
    rotation_policy: dict[str, Any] | None = Field(
        None, description="Automatic rotation policy"
    )


class SecretUpdateRequest(BaseModel):
    """Request model for updating an existing secret."""

    value: str = Field(..., min_length=1, description="New secret value")
    description: str | None = Field(None, description="Updated description")
    rotation_policy: dict[str, Any] | None = Field(
        None, description="Updated rotation policy"
    )


class SecretRotateRequest(BaseModel):
    """Request model for rotating a secret."""

    new_value: str = Field(
        ..., min_length=1, description="New secret value for rotation"
    )


class SecretResponse(BaseModel):
    """Response model for secret metadata."""

    name: str
    description: str | None
    created_at: str
    updated_at: str
    access_count: int | None = None
    last_accessed_at: str | None = None
    key_fingerprint: str | None = None
    has_rotation_policy: bool | None = None


class SecretValueResponse(BaseModel):
    """Response model for secret retrieval."""

    name: str
    value: str
    description: str | None
    access_count: int
    last_accessed_at: str | None


class AuditLogResponse(BaseModel):
    """Response model for audit log entries."""

    secret_name: str
    action: str
    user_id: UUID | None
    ip_address: str | None
    user_agent: str | None
    timestamp: str
    details: dict[str, Any] | None


# Dependency to get SecureVault instance
def get_secure_vault() -> SecureVault:
    """Get SecureVault instance."""
    try:
        return SecureVault()
    except MasterKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"SecureVault not available: {e}",
        ) from e


def get_request_context(request: Request) -> dict[str, Any]:
    """Extract request context for audit logging."""
    return {
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        # TODO(dev): Add user_id when authentication is implemented  # noqa: TD003,FIX002
        "user_id": None,
    }


@router.post("/", response_model=SecretResponse, status_code=status.HTTP_201_CREATED)
async def create_secret(
    request_data: SecretCreateRequest,
    request: Request,
    vault: SecureVault = Depends(get_secure_vault),  # noqa: B008
) -> SecretResponse:
    """Create a new encrypted secret.

    Args:
        request_data: Secret creation request
        request: HTTP request for context
        vault: SecureVault instance

    Returns:
        Created secret metadata

    Raises:
        400: If secret name already exists or validation fails
        503: If SecureVault is unavailable
    """
    try:
        context = get_request_context(request)
        secret = await vault.store_secret(
            name=request_data.name,
            value=request_data.value,
            description=request_data.description,
            rotation_policy=request_data.rotation_policy,
            **context,
        )

        return SecretResponse(
            name=secret.name,
            description=secret.description,
            created_at=secret.created_at.isoformat(),
            updated_at=secret.updated_at.isoformat(),
            access_count=secret.access_count,
            key_fingerprint=secret.key_fingerprint,
            has_rotation_policy=bool(secret.rotation_policy),
        )

    except SecretValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except SecretEncryptionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Encryption failed: {e}",
        ) from e


@router.get("/", response_model=list[SecretResponse])
async def list_secrets(
    include_metadata: bool = False,  # noqa: FBT001,FBT002
    request: Request | None = None,
    vault: SecureVault = Depends(get_secure_vault),  # noqa: B008
) -> list[SecretResponse]:
    """List all secrets with optional metadata.

    Args:
        include_metadata: Include access counts, timestamps, etc.
        request: HTTP request for context
        vault: SecureVault instance

    Returns:
        List of secret metadata (no values)
    """
    try:
        context = get_request_context(request) if request else {}
        secrets_data = await vault.list_secrets(
            include_metadata=include_metadata, **context
        )

        return [
            SecretResponse(
                name=str(secret_info["name"]),
                description=str(secret_info.get("description"))
                if secret_info.get("description") is not None
                else None,
                created_at=str(secret_info["created_at"]),
                updated_at=str(secret_info["updated_at"]),
                access_count=cast("int", secret_info["access_count"])
                if include_metadata and secret_info.get("access_count") is not None
                else None,
                last_accessed_at=str(secret_info.get("last_accessed_at"))
                if include_metadata and secret_info.get("last_accessed_at") is not None
                else None,
                key_fingerprint=str(secret_info.get("key_fingerprint"))
                if include_metadata and secret_info.get("key_fingerprint") is not None
                else None,
                has_rotation_policy=bool(secret_info.get("has_rotation_policy"))
                if include_metadata
                and secret_info.get("has_rotation_policy") is not None
                else None,
            )
            for secret_info in secrets_data
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list secrets: {e}",
        ) from e


@router.get("/{secret_name}", response_model=SecretValueResponse)
async def get_secret(
    secret_name: str,
    request: Request,
    vault: SecureVault = Depends(get_secure_vault),  # noqa: B008
) -> SecretValueResponse:
    """Retrieve and decrypt a secret value.

    Args:
        secret_name: Name of secret to retrieve
        request: HTTP request for context
        vault: SecureVault instance

    Returns:
        Decrypted secret value with metadata

    Raises:
        404: If secret not found
        500: If decryption fails
    """
    try:
        context = get_request_context(request)
        value = await vault.retrieve_secret(secret_name, **context)

        # Get updated secret metadata
        secrets_list = await vault.list_secrets(include_metadata=True, **context)
        secret_info = next((s for s in secrets_list if s["name"] == secret_name), None)

        if not secret_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Secret '{secret_name}' not found",
            )

        return SecretValueResponse(
            name=secret_name,
            value=value,
            description=str(secret_info.get("description"))
            if secret_info.get("description") is not None
            else None,
            access_count=cast("int", secret_info["access_count"])
            if secret_info.get("access_count") is not None
            else 0,
            last_accessed_at=str(secret_info.get("last_accessed_at"))
            if secret_info.get("last_accessed_at") is not None
            else None,
        )

    except SecretNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Secret '{secret_name}' not found",
        ) from e
    except SecretEncryptionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Decryption failed: {e}",
        ) from e


@router.put("/{secret_name}", response_model=SecretResponse)
async def update_secret(
    secret_name: str,
    request_data: SecretUpdateRequest,
    request: Request,
    vault: SecureVault = Depends(get_secure_vault),  # noqa: B008
) -> SecretResponse:
    """Update an existing secret value.

    Args:
        secret_name: Name of secret to update
        request_data: Updated secret data
        request: HTTP request for context
        vault: SecureVault instance

    Returns:
        Updated secret metadata

    Raises:
        404: If secret not found
        400: If validation fails
        500: If encryption fails
    """
    try:
        context = get_request_context(request)
        secret = await vault.update_secret(
            name=secret_name,
            new_value=request_data.value,
            description=request_data.description,
            rotation_policy=request_data.rotation_policy,
            **context,
        )

        return SecretResponse(
            name=secret.name,
            description=secret.description,
            created_at=secret.created_at.isoformat(),
            updated_at=secret.updated_at.isoformat(),
            access_count=secret.access_count,
            key_fingerprint=secret.key_fingerprint,
            has_rotation_policy=bool(secret.rotation_policy),
        )

    except SecretNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Secret '{secret_name}' not found",
        ) from e
    except SecretValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except SecretEncryptionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Encryption failed: {e}",
        ) from e


@router.post("/{secret_name}/rotate", response_model=SecretResponse)
async def rotate_secret(
    secret_name: str,
    request_data: SecretRotateRequest,
    request: Request,
    vault: SecureVault = Depends(get_secure_vault),  # noqa: B008
) -> SecretResponse:
    """Rotate a secret with new value and audit logging.

    Args:
        secret_name: Name of secret to rotate
        request_data: Rotation request with new value
        request: HTTP request for context
        vault: SecureVault instance

    Returns:
        Updated secret metadata

    Raises:
        404: If secret not found
        400: If validation fails
        500: If encryption fails
    """
    try:
        context = get_request_context(request)
        secret = await vault.rotate_secret(
            name=secret_name, new_value=request_data.new_value, **context
        )

        return SecretResponse(
            name=secret.name,
            description=secret.description,
            created_at=secret.created_at.isoformat(),
            updated_at=secret.updated_at.isoformat(),
            access_count=secret.access_count,
            key_fingerprint=secret.key_fingerprint,
            has_rotation_policy=bool(secret.rotation_policy),
        )

    except SecretNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Secret '{secret_name}' not found",
        ) from e
    except SecretValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except SecretEncryptionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Encryption failed: {e}",
        ) from e


@router.delete("/{secret_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_secret(
    secret_name: str,
    request: Request,
    vault: SecureVault = Depends(get_secure_vault),  # noqa: B008
) -> None:
    """Delete a secret permanently.

    Args:
        secret_name: Name of secret to delete
        request: HTTP request for context
        vault: SecureVault instance

    Raises:
        404: If secret not found
    """
    try:
        context = get_request_context(request)
        await vault.delete_secret(secret_name, **context)

    except SecretNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Secret '{secret_name}' not found",
        ) from e


@router.get("/{secret_name}/audit", response_model=list[AuditLogResponse])
async def get_secret_audit_logs(
    secret_name: str,
    action: str | None = None,
    limit: int = 100,
    vault: SecureVault = Depends(get_secure_vault),  # noqa: B008
) -> list[AuditLogResponse]:
    """Get audit logs for a specific secret.

    Args:
        secret_name: Name of secret to get logs for
        action: Filter by action type (READ, WRITE, ROTATE, DELETE)
        limit: Maximum number of log entries to return
        vault: SecureVault instance

    Returns:
        List of audit log entries
    """
    try:
        audit_logs = await vault.get_audit_logs(
            secret_name=secret_name, action=action, limit=limit
        )

        return [
            AuditLogResponse(
                secret_name=log.secret_name,
                action=log.action,
                user_id=log.user_id,
                ip_address=log.ip_address,
                user_agent=log.user_agent,
                timestamp=log.timestamp.isoformat(),
                details=log.details,
            )
            for log in audit_logs
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve audit logs: {e}",
        ) from e


@router.get("/audit/all", response_model=list[AuditLogResponse])
async def get_all_audit_logs(
    action: str | None = None,
    limit: int = 100,
    vault: SecureVault = Depends(get_secure_vault),  # noqa: B008
) -> list[AuditLogResponse]:
    """Get audit logs for all secret operations.

    Args:
        action: Filter by action type (READ, WRITE, ROTATE, DELETE)
        limit: Maximum number of log entries to return
        vault: SecureVault instance

    Returns:
        List of audit log entries
    """
    try:
        audit_logs = await vault.get_audit_logs(
            secret_name=None,  # All secrets
            action=action,
            limit=limit,
        )

        return [
            AuditLogResponse(
                secret_name=log.secret_name,
                action=log.action,
                user_id=log.user_id,
                ip_address=log.ip_address,
                user_agent=log.user_agent,
                timestamp=log.timestamp.isoformat(),
                details=log.details,
            )
            for log in audit_logs
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve audit logs: {e}",
        ) from e
