"""Configuration manager with SecureVault integration for runtime secret injection."""

import logging
import os
from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Any

from .exceptions import SecretNotFoundError
from .exceptions import SecureVaultError


if TYPE_CHECKING:
    from .vault import SecureVault
else:
    # Import at runtime to avoid circular dependencies
    from .vault import SecureVault


logger = logging.getLogger(__name__)


@dataclass
class SecretMapping:
    """Maps environment variable names to SecureVault secret names."""

    env_var: str
    secret_name: str
    default_value: str | None = None
    required: bool = True
    description: str = ""


@dataclass
class ConfigManager:
    """Manages configuration with SecureVault secret injection."""

    # Secret mappings for all application secrets
    secret_mappings: dict[str, SecretMapping] = field(
        default_factory=lambda: {
            # Database configuration
            "POSTGRES_PASSWORD": SecretMapping(
                env_var="POSTGRES_PASSWORD",
                secret_name="postgres_password",  # pragma: allowlist secret # nosec B106 # noqa: S106
                required=True,
                description="PostgreSQL database password",
            ),
            "POSTGRES_USER": SecretMapping(
                env_var="POSTGRES_USER",
                secret_name="postgres_user",  # pragma: allowlist secret # nosec B106 # noqa: S106
                default_value="ledgerly",
                required=False,
                description="PostgreSQL database username",
            ),
            # MinIO object storage
            "MINIO_ROOT_USER": SecretMapping(
                env_var="MINIO_ROOT_USER",
                secret_name="minio_root_user",  # pragma: allowlist secret # nosec B106 # noqa: S106
                default_value="minioadmin",
                required=False,
                description="MinIO root username",
            ),
            "MINIO_ROOT_PASSWORD": SecretMapping(
                env_var="MINIO_ROOT_PASSWORD",
                secret_name="minio_root_password",  # pragma: allowlist secret # nosec B106 # noqa: S106
                required=True,
                description="MinIO root password",
            ),
            # Redis cache
            "REDIS_PASSWORD": SecretMapping(
                env_var="REDIS_PASSWORD",
                secret_name="redis_password",  # pragma: allowlist secret # nosec B106 # noqa: S106
                required=False,
                description="Redis authentication password",
            ),
            # Application secrets
            "JWT_SECRET_KEY": SecretMapping(
                env_var="JWT_SECRET_KEY",
                secret_name="jwt_secret_key",  # pragma: allowlist secret # nosec B106 # noqa: S106
                required=True,
                description="JWT token signing key",
            ),
            "APP_SECRET_KEY": SecretMapping(
                env_var="APP_SECRET_KEY",
                secret_name="app_secret_key",  # pragma: allowlist secret # nosec B106 # noqa: S106
                required=True,
                description="Application secret key for encryption",
            ),
            # External API keys (for future use)
            "PLAID_SECRET": SecretMapping(
                env_var="PLAID_SECRET",
                secret_name="plaid_secret",  # pragma: allowlist secret # nosec B106 # noqa: S106
                required=False,
                description="Plaid API secret key",
            ),
            "PLAID_CLIENT_ID": SecretMapping(
                env_var="PLAID_CLIENT_ID",
                secret_name="plaid_client_id",  # pragma: allowlist secret # nosec B106 # noqa: S106
                required=False,
                description="Plaid API client ID",
            ),
        }
    )

    # Configuration cache
    _config_cache: dict[str, str] = field(default_factory=dict)
    _vault_available: bool = field(default=False)
    _vault_instance: Any | None = field(default=None)  # SecureVault instance

    def __post_init__(self) -> None:
        """Initialize configuration manager."""
        self._check_vault_availability()

    def _check_vault_availability(self) -> None:
        """Check if SecureVault is available and properly configured."""
        try:
            master_key = os.getenv("SECURE_VAULT_MASTER_KEY")
            if not master_key:
                logger.warning(
                    "SecureVault master key not found. Using environment variables only."
                )
                self._vault_available = False
                return

            # Using SecureVault imported at module level

            self._vault_instance = SecureVault(master_key)
            self._vault_available = True
            logger.info("SecureVault available for secret injection")

        except (ImportError, OSError, RuntimeError):
            logger.exception(
                "SecureVault unavailable. Falling back to environment variables."
            )
            self._vault_available = False

    async def load_secrets(self, *, force_reload: bool = False) -> None:
        """Load secrets from SecureVault into configuration cache.

        Args:
            force_reload: Force reload secrets even if already cached
        """
        if not force_reload and self._config_cache:
            logger.debug("Using cached configuration")
            return

        if not self._vault_available or not self._vault_instance:
            logger.warning(
                "SecureVault unavailable. Loading from environment variables only."
            )
            self._load_from_environment()
            return

        logger.info("Loading secrets from SecureVault...")

        for mapping in self.secret_mappings.values():
            try:
                # Try to get secret from SecureVault first
                secret_value = await self._vault_instance.retrieve_secret(
                    mapping.secret_name,
                    user_id=None,  # System operation
                    ip_address="127.0.0.1",
                    user_agent="ConfigManager",
                )

                self._config_cache[mapping.env_var] = secret_value
                # Also set environment variable for compatibility
                os.environ[mapping.env_var] = secret_value

                logger.debug(
                    "Loaded secret '%s' -> %s", mapping.secret_name, mapping.env_var
                )

            except SecretNotFoundError:
                # Secret not in vault, try environment or default
                env_value = os.getenv(mapping.env_var)
                if env_value:
                    self._config_cache[mapping.env_var] = env_value
                    logger.debug("Using environment value for %s", mapping.env_var)
                elif mapping.default_value:
                    self._config_cache[mapping.env_var] = mapping.default_value
                    os.environ[mapping.env_var] = mapping.default_value
                    logger.debug("Using default value for %s", mapping.env_var)
                elif mapping.required:
                    logger.exception(
                        "Required secret '%s' not found in vault or environment",
                        mapping.secret_name,
                    )
                    msg = f"Required secret '{mapping.secret_name}' not available"
                    raise SecureVaultError(msg) from None

            except (OSError, RuntimeError) as e:
                logger.exception("Error loading secret '%s'", mapping.secret_name)
                # Fall back to environment variable
                env_value = os.getenv(mapping.env_var)
                if env_value:
                    self._config_cache[mapping.env_var] = env_value
                elif mapping.required:
                    msg = f"Failed to load required secret '{mapping.secret_name}': {e}"
                    raise SecureVaultError(msg) from e

    def _load_from_environment(self) -> None:
        """Load configuration from environment variables only."""
        for mapping in self.secret_mappings.values():
            env_value = os.getenv(mapping.env_var)
            if env_value:
                self._config_cache[mapping.env_var] = env_value
            elif mapping.default_value:
                self._config_cache[mapping.env_var] = mapping.default_value
                os.environ[mapping.env_var] = mapping.default_value
            elif mapping.required:
                logger.error(
                    "Required environment variable %s not set", mapping.env_var
                )
                msg = f"Required environment variable {mapping.env_var} not set"
                raise SecureVaultError(msg)

    def get_config(self, key: str, default: str | None = None) -> str | None:
        """Get configuration value by key.

        Args:
            key: Configuration key (environment variable name)
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self._config_cache.get(key, default)

    def get_database_url(self) -> str:
        """Get PostgreSQL database URL."""
        user = self.get_config("POSTGRES_USER", "ledgerly")
        password = self.get_config("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db = os.getenv("POSTGRES_DB", "ledgerly")

        if not password:
            msg = "Database password not available"
            raise SecureVaultError(msg)

        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

    def get_redis_url(self) -> str:
        """Get Redis connection URL."""
        password = self.get_config("REDIS_PASSWORD")
        host = os.getenv("REDIS_HOST", "localhost")
        port = os.getenv("REDIS_PORT", "6379")
        db = os.getenv("REDIS_DB", "0")

        if password:
            return f"redis://:{password}@{host}:{port}/{db}"
        return f"redis://{host}:{port}/{db}"

    def get_minio_config(self) -> dict[str, Any]:
        """Get MinIO configuration."""
        return {
            "endpoint": os.getenv("MINIO_ENDPOINT", "localhost:9000"),
            "access_key": self.get_config("MINIO_ROOT_USER", "minioadmin"),
            "secret_key": self.get_config("MINIO_ROOT_PASSWORD", ""),
            "secure": os.getenv("MINIO_SECURE", "false").lower() == "true",
        }

    async def migrate_environment_secrets(self) -> dict[str, str]:
        """Migrate existing environment variable secrets to SecureVault.

        Returns:
            Dictionary of migrated secrets
        """
        if not self._vault_available or not self._vault_instance:
            msg = "SecureVault not available for migration"
            raise SecureVaultError(msg)

        migrated = {}

        for mapping in self.secret_mappings.values():
            env_value = os.getenv(mapping.env_var)
            if not env_value:
                logger.debug(
                    "No environment value for %s, skipping migration", mapping.env_var
                )
                continue

            try:
                # Check if secret already exists in vault
                try:
                    await self._vault_instance.retrieve_secret(mapping.secret_name)
                    logger.info(
                        "Secret '%s' already exists in vault, skipping migration",
                        mapping.secret_name,
                    )
                    continue
                except SecretNotFoundError:
                    pass  # Secret doesn't exist, proceed with migration

                # Store secret in vault
                await self._vault_instance.store_secret(
                    name=mapping.secret_name,
                    value=env_value,
                    description=mapping.description,
                    user_id=None,  # System migration
                    ip_address="127.0.0.1",
                    user_agent="ConfigManager-Migration",
                )

                migrated[mapping.secret_name] = mapping.env_var
                logger.info(
                    "Migrated %s -> '%s' to SecureVault",
                    mapping.env_var,
                    mapping.secret_name,
                )

            except (OSError, RuntimeError):
                logger.exception("Failed to migrate %s", mapping.env_var)
                raise

        return migrated

    def is_vault_available(self) -> bool:
        """Check if SecureVault is available."""
        return self._vault_available

    def get_secret_mappings(self) -> dict[str, SecretMapping]:
        """Get all secret mappings."""
        return self.secret_mappings.copy()


# Global configuration manager instance
config_manager = ConfigManager()


async def initialize_config() -> ConfigManager:
    """Initialize configuration with secret injection.

    Returns:
        Configured ConfigManager instance
    """
    await config_manager.load_secrets()
    return config_manager


def get_config_manager() -> ConfigManager:
    """Get the global configuration manager instance."""
    return config_manager
