"""Database seeding script for initial data."""

import asyncio
import logging
from uuid import UUID

import database
from models.orm import AccountType
from models.orm import Base
from models.orm import Institution


# Set up logging for seed output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Predefined UUIDs for consistency with database schema documentation
INSTITUTION_IDS = {
    "citi": UUID("550e8400-e29b-41d4-a716-446655440000"),
    "chase": UUID("550e8400-e29b-41d4-a716-446655440001"),
    "boa": UUID("550e8400-e29b-41d4-a716-446655440002"),
}

ACCOUNT_TYPE_IDS = {
    "credit_card": UUID("660e8400-e29b-41d4-a716-446655440000"),
    "checking": UUID("660e8400-e29b-41d4-a716-446655440001"),
    "savings": UUID("660e8400-e29b-41d4-a716-446655440002"),
}


async def seed_institutions() -> None:
    """Seed institutions table with default data."""
    async with database.async_session_maker() as session:
        institutions = [
            Institution(
                id=INSTITUTION_IDS["citi"],
                name="Citibank",
                slug="citi",
                website="https://www.citi.com",
            ),
            Institution(
                id=INSTITUTION_IDS["chase"],
                name="Chase",
                slug="chase",
                website="https://www.chase.com",
            ),
            Institution(
                id=INSTITUTION_IDS["boa"],
                name="Bank of America",
                slug="boa",
                website="https://www.bankofamerica.com",
            ),
        ]

        session.add_all(institutions)
        await session.commit()
        logger.info("✅ Seeded institutions")


async def seed_account_types() -> None:
    """Seed account types table with default data."""
    async with database.async_session_maker() as session:
        account_types = [
            AccountType(
                id=ACCOUNT_TYPE_IDS["credit_card"],
                name="Credit Card",
                slug="credit_card",
                description="Standard credit card account",
                parser_config={"supports_pdf": True, "supports_csv": True},
            ),
            AccountType(
                id=ACCOUNT_TYPE_IDS["checking"],
                name="Checking Account",
                slug="checking",
                description="Standard checking account",
                parser_config={"supports_pdf": True, "supports_csv": True},
            ),
            AccountType(
                id=ACCOUNT_TYPE_IDS["savings"],
                name="Savings Account",
                slug="savings",
                description="Standard savings account",
                parser_config={"supports_pdf": True, "supports_csv": True},
            ),
        ]

        session.add_all(account_types)
        await session.commit()
        logger.info("✅ Seeded account types")


async def seed_database() -> None:
    """Seed the database with initial data."""
    logger.info("🌱 Starting database seeding...")

    # Ensure all tables exist
    async with database.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        await seed_institutions()
        await seed_account_types()
        logger.info("🎉 Database seeding completed successfully!")
    except Exception:
        logger.exception("❌ Error during seeding")
        raise


if __name__ == "__main__":
    asyncio.run(seed_database())
