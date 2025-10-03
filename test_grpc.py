#!/usr/bin/env python3
"""Test script to verify gRPC communication between Telegram bot and backend."""

import asyncio
import logging
import sys

# Add paths for imports
sys.path.append('.')

from src.telegram_bot.services.grpc_client import BackendGRPCClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_grpc_connection():
    """Test all gRPC methods."""
    print("\n" + "="*50)
    print("Testing gRPC Connection")
    print("="*50 + "\n")

    client = BackendGRPCClient()

    try:
        # Test 1: Ping
        print("1. Testing Ping...")
        response = await client.ping("Test message from script")
        if response:
            print(f"   ✅ Ping successful: {response}")
        else:
            print("   ❌ Ping failed")

        # Test 2: Get non-existent user
        print("\n2. Testing GetUserState (non-existent)...")
        user_state = await client.get_user_state(999999999)
        if user_state is None:
            print("   ✅ Correctly returned None for non-existent user")
        else:
            print(f"   ❌ Unexpected result: {user_state}")

        # Test 3: Register new user
        print("\n3. Testing RegisterUser...")
        result = await client.register_user(123456789, "testuser")
        if result and result['success']:
            print(f"   ✅ User registered: {result}")
            user_id = result['user_id']
        else:
            print(f"   ❌ Registration failed: {result}")
            return

        # Test 4: Get existing user
        print("\n4. Testing GetUserState (existing)...")
        user_state = await client.get_user_state(123456789)
        if user_state:
            print(f"   ✅ User found: {user_state}")
        else:
            print("   ❌ User not found")

        # Test 5: Connect wallet
        print("\n5. Testing ConnectWallet...")
        wallet_result = await client.connect_wallet(
            user_id,
            "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb4",
            "metamask"
        )
        if wallet_result and wallet_result['success']:
            print(f"   ✅ Wallet connected: {wallet_result}")
        else:
            print(f"   ❌ Wallet connection failed: {wallet_result}")

        # Test 6: Classify intent
        print("\n6. Testing ClassifyIntent...")
        intent_result = await client.classify_intent(
            "I want to invest $500 in a safe strategy",
            123456789
        )
        if intent_result:
            print(f"   ✅ Intent classified: {intent_result}")
        else:
            print("   ❌ Intent classification failed")

        print("\n" + "="*50)
        print("All tests completed successfully! ✅")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        logger.exception("Test error")
    finally:
        client.close()


if __name__ == "__main__":
    print("\nStarting gRPC test...")
    print("Make sure the backend is running on port 50051")
    print("Run with: python -m src.backend.main")

    asyncio.run(test_grpc_connection())