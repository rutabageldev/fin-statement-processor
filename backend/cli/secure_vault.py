#!/usr/bin/env python3
"""Command-line interface for SecureVault secret management."""

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path


# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.secure_vault import SecureVault
from services.secure_vault import SecureVaultEncryption
from services.secure_vault.config_manager import ConfigManager
from services.secure_vault.exceptions import MasterKeyError
from services.secure_vault.exceptions import SecretNotFoundError
from services.secure_vault.exceptions import SecretValidationError


def setup_logging() -> logging.Logger:
    """Set up logging for the CLI."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",  # Clean format for CLI output
    )
    return logging.getLogger(__name__)


def console_output(message: str) -> None:
    """Output message to console."""
    # For CLI tools, direct output to stdout is appropriate
    sys.stdout.write(f"{message}\n")
    sys.stdout.flush()


def console_error(message: str) -> None:
    """Output error message to console."""
    sys.stderr.write(f"{message}\n")
    sys.stderr.flush()


async def create_secret(
    vault: SecureVault, name: str, value: str, description: str | None = None
) -> None:
    """Create a new secret."""
    try:
        secret = await vault.store_secret(
            name=name,
            value=value,
            description=description,
            user_id=None,
            ip_address="127.0.0.1",
            user_agent="SecureVault-CLI",
        )
        console_output(f"✓ Secret '{name}' created successfully")
        console_output(f"  ID: {secret.id}")
        console_output(f"  Created: {secret.created_at}")

    except SecretValidationError as e:
        console_error(f"✗ Validation error: {e}")
        sys.exit(1)
    except (OSError, RuntimeError) as e:
        console_error(f"✗ Failed to create secret: {e}")
        sys.exit(1)


async def get_secret(vault: SecureVault, name: str) -> None:
    """Retrieve and display a secret."""
    try:
        value = await vault.retrieve_secret(
            name=name,
            user_id=None,
            ip_address="127.0.0.1",
            user_agent="SecureVault-CLI",
        )
        console_output(f"Secret '{name}': {value}")

    except SecretNotFoundError:
        console_error(f"✗ Secret '{name}' not found")
        sys.exit(1)
    except (OSError, RuntimeError) as e:
        console_error(f"✗ Failed to retrieve secret: {e}")
        sys.exit(1)


async def list_secrets(vault: SecureVault, *, show_metadata: bool = False) -> None:
    """List all secrets."""
    try:
        secrets = await vault.list_secrets(
            include_metadata=show_metadata,
            user_id=None,
            ip_address="127.0.0.1",
            user_agent="SecureVault-CLI",
        )

        if not secrets:
            console_output("No secrets found")
            return

        console_output(f"Found {len(secrets)} secrets:")
        console_output("")

        for secret in secrets:
            console_output(f"Name: {secret['name']}")
            if secret.get("description"):
                console_output(f"  Description: {secret['description']}")
            console_output(f"  Created: {secret['created_at']}")
            console_output(f"  Updated: {secret['updated_at']}")

            if show_metadata:
                console_output(f"  Access Count: {secret.get('access_count', 0)}")
                if secret.get("last_accessed_at"):
                    console_output(f"  Last Accessed: {secret['last_accessed_at']}")
                if secret.get("key_fingerprint"):
                    console_output(f"  Key Fingerprint: {secret['key_fingerprint']}")
                if secret.get("has_rotation_policy"):
                    console_output("  Has Rotation Policy: Yes")
            console_output("")

    except (OSError, RuntimeError) as e:
        console_error(f"✗ Failed to list secrets: {e}")
        sys.exit(1)


async def delete_secret(
    vault: SecureVault, name: str, *, confirm: bool = False
) -> None:
    """Delete a secret."""
    if not confirm:
        response = input(f"Are you sure you want to delete secret '{name}'? (y/N): ")
        if response.lower() != "y":
            console_output("Cancelled")
            return

    try:
        await vault.delete_secret(
            name=name,
            user_id=None,
            ip_address="127.0.0.1",
            user_agent="SecureVault-CLI",
        )
        console_output(f"✓ Secret '{name}' deleted successfully")

    except SecretNotFoundError:
        console_error(f"✗ Secret '{name}' not found")
        sys.exit(1)
    except (OSError, RuntimeError) as e:
        console_error(f"✗ Failed to delete secret: {e}")
        sys.exit(1)


async def rotate_secret(vault: SecureVault, name: str, new_value: str) -> None:
    """Rotate a secret with new value."""
    try:
        secret = await vault.rotate_secret(
            name=name,
            new_value=new_value,
            user_id=None,
            ip_address="127.0.0.1",
            user_agent="SecureVault-CLI",
        )
        console_output(f"✓ Secret '{name}' rotated successfully")
        console_output(f"  Updated: {secret.updated_at}")

    except SecretNotFoundError:
        console_error(f"✗ Secret '{name}' not found")
        sys.exit(1)
    except (OSError, RuntimeError) as e:
        console_error(f"✗ Failed to rotate secret: {e}")
        sys.exit(1)


async def show_audit_logs(
    vault: SecureVault,
    secret_name: str | None = None,
    action: str | None = None,
    limit: int = 100,
) -> None:
    """Show audit logs."""
    try:
        logs = await vault.get_audit_logs(
            secret_name=secret_name, action=action, limit=limit
        )

        if not logs:
            console_output("No audit logs found")
            return

        console_output(f"Found {len(logs)} audit log entries:")
        console_output("")

        for log in logs:
            console_output(f"Timestamp: {log.timestamp}")
            console_output(f"  Secret: {log.secret_name}")
            console_output(f"  Action: {log.action}")
            if log.ip_address:
                console_output(f"  IP Address: {log.ip_address}")
            if log.user_agent:
                console_output(f"  User Agent: {log.user_agent}")
            if log.details:
                console_output(f"  Details: {log.details}")
            console_output("")

    except (OSError, RuntimeError) as e:
        console_error(f"✗ Failed to retrieve audit logs: {e}")
        sys.exit(1)


async def migrate_environment_secrets(config_manager: ConfigManager) -> None:
    """Migrate environment variable secrets to SecureVault."""
    try:
        if not config_manager.is_vault_available():
            console_output("✗ SecureVault is not available. Cannot perform migration.")
            sys.exit(1)

        console_output("Migrating environment variable secrets to SecureVault...")
        migrated = await config_manager.migrate_environment_secrets()

        if migrated:
            console_output(f"✓ Successfully migrated {len(migrated)} secrets:")
            for secret_name, env_var in migrated.items():
                console_output(f"  {env_var} -> '{secret_name}'")
        else:
            console_output("No secrets to migrate (all secrets already in vault)")

    except (OSError, RuntimeError) as e:
        console_error(f"✗ Migration failed: {e}")
        sys.exit(1)


def generate_master_key() -> None:
    """Generate a new master key."""
    key = SecureVaultEncryption.generate_master_key()
    console_output("Generated master key:")
    console_output(key)
    console_output("")
    console_output("Add this to your .env file:")
    console_output(f"SECURE_VAULT_MASTER_KEY={key}")


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="SecureVault CLI - Manage encrypted secrets"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate master key
    subparsers.add_parser("generate-key", help="Generate a new master key")

    # Create secret
    create_parser = subparsers.add_parser("create", help="Create a new secret")
    create_parser.add_argument("name", help="Secret name")
    create_parser.add_argument("value", help="Secret value")
    create_parser.add_argument("--description", help="Secret description")

    # Get secret
    get_parser = subparsers.add_parser("get", help="Retrieve a secret value")
    get_parser.add_argument("name", help="Secret name")

    # List secrets
    list_parser = subparsers.add_parser("list", help="List all secrets")
    list_parser.add_argument("--metadata", action="store_true", help="Include metadata")

    # Delete secret
    delete_parser = subparsers.add_parser("delete", help="Delete a secret")
    delete_parser.add_argument("name", help="Secret name")
    delete_parser.add_argument("--yes", action="store_true", help="Skip confirmation")

    # Rotate secret
    rotate_parser = subparsers.add_parser(
        "rotate", help="Rotate a secret with new value"
    )
    rotate_parser.add_argument("name", help="Secret name")
    rotate_parser.add_argument("new_value", help="New secret value")

    # Audit logs
    audit_parser = subparsers.add_parser("audit", help="Show audit logs")
    audit_parser.add_argument("--secret", help="Filter by secret name")
    audit_parser.add_argument("--action", help="Filter by action type")
    audit_parser.add_argument(
        "--limit", type=int, default=100, help="Limit number of results"
    )

    # Migration
    subparsers.add_parser("migrate", help="Migrate environment secrets to SecureVault")

    return parser


async def execute_vault_command(args: argparse.Namespace) -> None:
    """Execute vault commands that require a SecureVault instance."""
    # Check if master key is available
    master_key = os.getenv("SECURE_VAULT_MASTER_KEY")
    if not master_key:
        console_output("✗ SECURE_VAULT_MASTER_KEY environment variable not set")
        console_output(
            "Run 'python cli/secure_vault.py generate-key' to generate a new key"
        )
        sys.exit(1)

    vault = SecureVault(master_key)

    if args.command == "create":
        await create_secret(vault, args.name, args.value, args.description)
    elif args.command == "get":
        await get_secret(vault, args.name)
    elif args.command == "list":
        await list_secrets(vault, show_metadata=args.metadata)
    elif args.command == "delete":
        await delete_secret(vault, args.name, confirm=args.yes)
    elif args.command == "rotate":
        await rotate_secret(vault, args.name, args.new_value)
    elif args.command == "audit":
        await show_audit_logs(vault, args.secret, args.action, args.limit)
    elif args.command == "migrate":
        config_manager = ConfigManager()
        await migrate_environment_secrets(config_manager)


async def main() -> None:
    """Main CLI function."""
    parser = create_argument_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "generate-key":
        generate_master_key()
        return

    # Commands that need vault instance
    try:
        await execute_vault_command(args)
    except MasterKeyError as e:
        console_error(f"✗ Master key error: {e}")
        sys.exit(1)
    except (OSError, RuntimeError) as e:
        console_error(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
