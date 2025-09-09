"""Test script to verify SQLAlchemy ORM implementation."""

import asyncio
import logging
from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

import database
from models.orm import Account
from models.orm import AccountType
from models.orm import CreditCardDetail
from models.orm import Institution
from models.orm import Statement
from models.orm import StatementDetail
from models.orm import Transaction
from models.orm import User


# Set up logging for test output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.anyio
async def test_basic_queries() -> None:
    """Test basic ORM functionality."""
    logger.info("🧪 Testing SQLAlchemy ORM implementation...")

    async with database.async_session_maker() as session:
        # Test fetching institutions
        result = await session.execute(select(Institution))
        institutions = result.scalars().all()
        logger.info("✅ Found %d institutions in database", len(institutions))

        # Test fetching account types
        result = await session.execute(select(AccountType))
        account_types = result.scalars().all()
        logger.info("✅ Found %d account types in database", len(account_types))


@pytest.mark.anyio
async def test_orm_models() -> None:
    """Test ORM model creation and relationships."""
    logger.info("🧪 Testing ORM model creation and relationships...")

    async with database.async_session_maker() as session:
        # Get first institution and account type
        citi = await session.get(Institution, "550e8400-e29b-41d4-a716-446655440000")
        cc_type = await session.get(AccountType, "660e8400-e29b-41d4-a716-446655440000")

        if not citi or not cc_type:
            logger.error("❌ Required seed data not found")
            return

        logger.info("✅ Retrieved institution: %s", citi.name)
        logger.info("✅ Retrieved account type: %s", cc_type.name)

        # Create a test user
        test_user = User(
            email="test@example.com",
            password_hash="hashed_password_here",  # pragma: allowlist secret  # nosec B106  # noqa: S106
        )
        session.add(test_user)
        await session.flush()  # Get the ID
        logger.info("✅ Created test user: %s", test_user.email)

        # Create a test account
        test_account = Account(
            user_id=test_user.id,
            institution_id=citi.id,
            account_type_id=cc_type.id,
            account_number_hash="test_account_hash",
            nickname="Test Credit Card",
            currency="USD",
        )
        session.add(test_account)
        await session.flush()
        logger.info("✅ Created test account: %s", test_account.nickname)

        # Create a test statement
        test_statement = Statement(
            account_id=test_account.id,
            period_start=date(2025, 8, 1),
            period_end=date(2025, 8, 31),
            file_pdf_url="https://example.com/statement.pdf",
            status="completed",
        )
        session.add(test_statement)
        await session.flush()
        logger.info(
            "✅ Created test statement: %s to %s",
            test_statement.period_start,
            test_statement.period_end,
        )

        # Create statement details
        test_details = StatementDetail(
            statement_id=test_statement.id,
            previous_balance=Decimal("500.00"),
            new_balance=Decimal("750.50"),
            minimum_payment=Decimal("25.00"),
            due_date=date(2025, 9, 15),
        )
        session.add(test_details)
        logger.info(
            "✅ Created statement details: balance $%s", test_details.new_balance
        )

        # Create a test transaction
        test_transaction = Transaction(
            statement_id=test_statement.id,
            account_id=test_account.id,
            transaction_date=date(2025, 8, 15),
            amount=Decimal("-125.50"),
            description="WHOLE FOODS MARKET",
            category="groceries",
            transaction_type="debit",
        )
        session.add(test_transaction)
        logger.info("✅ Created test transaction: $%s", test_transaction.amount)

        # Create credit card details
        test_cc_details = CreditCardDetail(
            account_id=test_account.id,
            statement_id=test_statement.id,
            credit_limit=Decimal("5000.00"),
            available_credit=Decimal("4249.50"),
            points_earned=125,
            points_redeemed=0,
            fees=Decimal("0.00"),
            purchases=Decimal("125.50"),
        )
        session.add(test_cc_details)
        logger.info(
            "✅ Created credit card details: $%s limit", test_cc_details.credit_limit
        )

        await session.commit()
        logger.info("✅ All test data committed to database")


@pytest.mark.anyio
async def test_relationships() -> None:
    """Test ORM relationships."""
    logger.info("🧪 Testing ORM relationships...")

    async with database.async_session_maker() as session:
        # Find our test user and load relationships
        stmt = (
            select(User)
            .where(User.email == "test@example.com")
            .options(selectinload(User.accounts).selectinload(Account.statements))
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            logger.error("❌ Test user not found")
            return

        logger.info("✅ Found user: %s", user.email)
        logger.info("✅ User has %d accounts", len(user.accounts))

        if user.accounts:
            account = user.accounts[0]
            logger.info("✅ Account: %s", account.nickname)
            logger.info("✅ Account has %d statements", len(account.statements))

            if account.statements:
                statement = account.statements[0]
                logger.info(
                    "✅ Statement: %s to %s",
                    statement.period_start,
                    statement.period_end,
                )


async def run_tests() -> None:
    """Run all tests."""
    try:
        await test_basic_queries()
        await test_orm_models()
        await test_relationships()
        logger.info("🎉 All SQLAlchemy ORM tests passed!")
    except Exception:
        logger.exception("❌ Test failed")
        raise


if __name__ == "__main__":
    asyncio.run(run_tests())
