"""Test script for onboarding flow using gRPC client."""

import asyncio
import logging
from uuid import uuid4

from src.telegram_bot.services.grpc_client import get_grpc_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_onboarding_flow():
    """Test the complete onboarding flow."""
    client = get_grpc_client()

    # Test 1: Ping server
    logger.info("Test 1: Testing ping...")
    response = await client.ping("Hello from test!")
    logger.info(f"Ping response: {response}")
    assert response is not None, "Ping failed"

    # Test 2: Check new user state
    test_telegram_id = 123456789
    logger.info(f"\nTest 2: Checking state for new user {test_telegram_id}...")
    state = await client.get_user_state(test_telegram_id)
    logger.info(f"User state: {state}")

    # Test 3: Register user (or get existing)
    logger.info(f"\nTest 3: Registering user {test_telegram_id}...")
    result = await client.register_user(test_telegram_id, "testuser")
    logger.info(f"Register result: {result}")

    if state is None:
        # New user
        assert result and result['success'], "User registration failed"
        user_id = result['user_id']
        logger.info(f"User registered with ID: {user_id}")
    else:
        # Existing user
        logger.info(f"User already exists with ID: {state['user_id']}")
        user_id = state['user_id']

    # Test 4: Check user state after registration
    logger.info(f"\nTest 4: Checking state after registration...")
    state = await client.get_user_state(test_telegram_id)
    logger.info(f"User state: {state}")
    assert state is not None, "User should exist after registration"
    # State could be NEW if just registered, or FUNDED if already has wallet

    # Test 5: Connect wallet
    wallet_address = f"0x{uuid4().hex[:40]}"
    logger.info(f"\nTest 5: Connecting wallet {wallet_address}...")
    result = await client.connect_wallet(user_id, wallet_address, "manual")
    logger.info(f"Wallet connection result: {result}")
    assert result and result['success'], "Wallet connection failed"

    # Test 6: Check state after wallet connection
    logger.info(f"\nTest 6: Checking state after wallet connection...")
    state = await client.get_user_state(test_telegram_id)
    logger.info(f"User state: {state}")
    # Wallet address should be updated to new one OR existing one
    assert state.get('wallet_address'), "Wallet address should be set"
    assert state['balance'] > 0, "Balance should be updated"
    logger.info(f"User balance: ${state['balance']}")

    # Test 7: Test intent classification
    logger.info(f"\nTest 7: Testing intent classification...")
    result = await client.classify_intent("I want to connect my wallet", test_telegram_id)
    logger.info(f"Intent classification: {result}")
    assert result and result['domain'] == 'ONBOARDING', "Should classify as onboarding intent"

    logger.info("\n✅ All tests passed! Onboarding flow is working correctly.")


if __name__ == "__main__":
    asyncio.run(test_onboarding_flow())