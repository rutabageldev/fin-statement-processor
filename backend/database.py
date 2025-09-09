"""Database configuration and session management for Ledgerly."""

import os
from collections.abc import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

# Import base for easy access
from models.orm.base import Base
from services.secure_vault.config_manager import get_config_manager


class DatabaseConfig:
    """Database configuration and session management."""

    def __init__(self) -> None:
        """Initialize database configuration."""
        # Try to get database URL from config manager (with SecureVault integration)
        try:
            config_manager = get_config_manager()
            self.database_url = config_manager.get_database_url()
        except Exception:  # noqa: BLE001
            # Fallback to environment variable or default
            self.database_url = os.getenv(
                "DATABASE_URL",
                "postgresql://postgres:dev_password@localhost:5432/ledgerly",  # pragma: allowlist secret
            )

        self.async_database_url = self.database_url.replace(
            "postgresql://", "postgresql+asyncpg://"
        )

        # Configure async engine with better connection settings
        self.async_engine: AsyncEngine = create_async_engine(
            self.async_database_url,
            echo=os.getenv("LOG_LEVEL", "INFO") == "DEBUG",
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
        )

        # Use async_sessionmaker for SQLAlchemy 2.0+
        self.async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

        # Sync engine for migrations and CLI operations
        self.sync_engine = create_engine(
            self.database_url.replace("postgresql://", "postgresql+psycopg2://"),
            echo=os.getenv("LOG_LEVEL", "INFO") == "DEBUG",
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
        )

        # Sync session maker
        self.sync_session_maker: sessionmaker[Session] = sessionmaker(
            bind=self.sync_engine,
            autocommit=False,
            autoflush=False,
        )

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get async database session for dependency injection."""
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    def get_sync_session(self) -> sessionmaker[Session]:
        """Get synchronous database session maker for migrations and setup."""
        return self.sync_session_maker

    async def create_tables(self) -> None:
        """Create all tables in the database."""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self) -> None:
        """Drop all tables in the database."""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


# Global instance for backward compatibility
db = DatabaseConfig()

# Expose module-level access for backward compatibility
async_engine = db.async_engine
async_session_maker = db.async_session_maker
sync_engine = db.sync_engine
sync_session_maker = db.sync_session_maker
get_async_session = db.get_async_session
get_sync_session = db.get_sync_session
create_tables = db.create_tables
drop_tables = db.drop_tables


# Module exports for mypy
__all__ = [
    "Base",
    "DatabaseConfig",
    "async_engine",
    "async_session_maker",
    "create_tables",
    "db",
    "drop_tables",
    "get_async_session",
    "get_sync_session",
]
