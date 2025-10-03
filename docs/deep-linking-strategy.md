# Deep Linking Strategy: Telegram Bot ↔ Web App Integration

## Overview

This document outlines the deep linking strategy for seamless integration between the Agent x402 Telegram bot and the companion web application. The goal is to provide a frictionless user experience where users can transition between Telegram and the web dashboard while maintaining context and authentication state.

## Architecture Principles

### 1. **Wallet-Based Identity**
- Single source of truth: **Ethereum wallet address**
- No separate email/password authentication
- Consistent user identity across all platforms

### 2. **Secure Token Exchange**
- Short-lived, single-use tokens for Telegram → Web transitions
- JWT tokens for web session management
- Token expiration: 5 minutes for deep link tokens, 24 hours for session JWTs

### 3. **Context Preservation**
- Deep links carry contextual information (agent ID, mandate ID, transaction hash)
- User lands on the exact resource they clicked from Telegram

---

## Deep Linking Flows

### Flow 1: View Agent Performance (Telegram → Web)

**Trigger:** User in Telegram asks "Show me my DCA agent's performance"

**Telegram Bot Response:**
```text
📊 Your DCA Agent is up +12.5% this month!

💰 Total Trades: 47
✅ Win Rate: 68%
📈 ROI: +12.5%

[View Detailed Dashboard →]
```

**Deep Link Structure:**
```text
https://app.agentx402.com/agents/{agent_id}?auth={short_lived_token}
```

**Backend Flow:**
1. Telegram bot calls `/api/v1/auth/create-web-token`
   ```json
   {
     "telegram_user_id": "123456789",
     "wallet_address": "0x742d...",
     "target_resource": "agent",
     "resource_id": "uuid-of-agent",
     "expires_in": 300
   }
   ```

2. Backend generates short-lived token (5 min expiry)
   ```json
   {
     "token": "eyJhbGc...",
     "deep_link": "https://app.agentx402.com/agents/uuid?auth=eyJhbGc..."
   }
   ```

3. User clicks link → Web app receives token

4. Web app calls `/api/v1/auth/exchange-token`
   ```json
   {
     "short_lived_token": "eyJhbGc..."
   }
   ```

5. Backend validates token, returns session JWT
   ```json
   {
     "session_token": "eyJhbGc...",
     "user": {
       "wallet_address": "0x742d...",
       "telegram_user_id": "123456789"
     },
     "expires_at": "2025-10-04T08:00:00Z"
   }
   ```

6. Web app stores JWT in localStorage, user is authenticated

**Web App Behavior:**
- If token valid: Auto-login + navigate to agent dashboard
- If token expired: Show "Connect Wallet" button with friendly message
- If token invalid: Show error, redirect to home

---

### Flow 2: Create Mandate (Web → Telegram Notification)

**Trigger:** User creates mandate in web app

**Web App Flow:**
1. User fills out mandate form in web dashboard
2. Submits mandate creation
3. Backend creates mandate, emits event

**Backend Event:**
```json
{
  "event": "mandate.created",
  "user_id": "uuid",
  "wallet_address": "0x742d...",
  "mandate_id": "uuid",
  "telegram_user_id": "123456789"
}
```

**Telegram Notification:**
```text
✅ New Mandate Created

Strategy: DCA Grid Trading
Budget: $500 USDC
Risk Level: Moderate

Your agent is ready to start trading!

[View Mandate] [Start Agent]
```

**Action Buttons:**
- `[View Mandate]` → Deep link back to web app
- `[Start Agent]` → Inline Telegram action (activates agent via bot)

---

### Flow 3: Sign Transaction (Web → Telegram Mini App)

**Trigger:** User needs to sign mandate in web app

**Web App shows:**
```text
⚠️ Signature Required

To activate this mandate, you need to sign with your wallet.

[Sign with Telegram] [Sign with MetaMask]
```

**Option 1: Sign with Telegram**
- Opens Telegram Mini App
- Uses Telegram Wallet or connected wallet
- Signs message, returns signature to web

**Option 2: Sign with MetaMask**
- Standard WalletConnect flow
- User signs in web browser
- No Telegram integration needed

**Deep Link to Telegram Mini App:**
```text
https://t.me/{bot_username}/sign?mandate_id={uuid}&nonce={nonce}&callback=https://app.agentx402.com/mandates/{uuid}/confirm
```

---

## URL Structure Patterns

### General Pattern
```text
https://app.agentx402.com/{resource_type}/{resource_id}?auth={token}&action={optional_action}
```

### Examples

**Agent Dashboard:**
```text
https://app.agentx402.com/agents/550e8400-e29b-41d4-a716-446655440000?auth=eyJhbGc...
```

**Mandate Details:**
```text
https://app.agentx402.com/mandates/650e8400-e29b-41d4-a716-446655440001?auth=eyJhbGc...
```

**Trade History:**
```text
https://app.agentx402.com/agents/550e8400/trades?auth=eyJhbGc...&filter=last_7_days
```

**Portfolio Overview:**
```text
https://app.agentx402.com/portfolio?auth=eyJhbGc...
```

**Transaction Details:**
```text
https://app.agentx402.com/tx/0x1234...?auth=eyJhbGc...
```

---

## Authentication Token Types

### 1. Short-Lived Deep Link Token
**Purpose:** Telegram → Web transitions

**Properties:**
- **Expiry:** 5 minutes
- **Single-use:** Consumed on first exchange
- **Claims:**
  ```json
  {
    "type": "deep_link",
    "telegram_user_id": "123456789",
    "wallet_address": "0x742d...",
    "target_resource": "agent",
    "resource_id": "uuid",
    "iat": 1696310400,
    "exp": 1696310700
  }
  ```

### 2. Session JWT
**Purpose:** Web app session persistence

**Properties:**
- **Expiry:** 24 hours
- **Renewable:** Can be refreshed
- **Claims:**
  ```json
  {
    "type": "session",
    "user_id": "uuid",
    "wallet_address": "0x742d...",
    "telegram_user_id": "123456789",
    "iat": 1696310400,
    "exp": 1696396800
  }
  ```

### 3. Telegram Mini App Init Data
**Purpose:** Telegram Mini App authentication

**Properties:**
- **Validation:** Via Telegram Bot API
- **Format:** URL-encoded init data from Telegram
- **Example:**
  ```text
  query_id=AAH...&user={"id":123456789,"first_name":"John"}&auth_date=1696310400&hash=abcd1234...
  ```

---

## API Endpoints (Backend)

### POST `/api/v1/auth/create-web-token`
Create deep link token for Telegram → Web transition

**Request:**
```json
{
  "telegram_user_id": "123456789",
  "wallet_address": "0x742d...",
  "target_resource": "agent",
  "resource_id": "uuid"
}
```

**Response:**
```json
{
  "token": "eyJhbGc...",
  "deep_link": "https://app.agentx402.com/agents/uuid?auth=eyJhbGc...",
  "expires_at": "2025-10-03T08:15:00Z"
}
```

---

### POST `/api/v1/auth/exchange-token`
Exchange deep link token for session JWT

**Request:**
```json
{
  "short_lived_token": "eyJhbGc..."
}
```

**Response:**
```json
{
  "session_token": "eyJhbGc...",
  "user": {
    "id": "uuid",
    "wallet_address": "0x742d...",
    "telegram_user_id": "123456789"
  },
  "expires_at": "2025-10-04T08:00:00Z"
}
```

**Error Responses:**
- `401 Unauthorized` - Token expired or invalid
- `409 Conflict` - Token already used

---

### POST `/api/v1/auth/wallet-login`
Authenticate via wallet signature

**Request:**
```json
{
  "wallet_address": "0x742d...",
  "message": "Sign in to Agent x402\nNonce: abc123",
  "signature": "0x..."
}
```

**Response:**
```json
{
  "session_token": "eyJhbGc...",
  "user": {
    "id": "uuid",
    "wallet_address": "0x742d...",
    "telegram_user_id": "123456789"
  }
}
```

---

### POST `/api/v1/auth/refresh-token`
Refresh session JWT

**Request:**
```json
{
  "refresh_token": "eyJhbGc..."
}
```

**Response:**
```json
{
  "session_token": "eyJhbGc...",
  "expires_at": "2025-10-04T08:00:00Z"
}
```

---

## Database Schema Updates

### Table: `deep_link_tokens`
```sql
CREATE TABLE deep_link_tokens (
    id UUID PRIMARY KEY,
    token_hash VARCHAR(64) NOT NULL UNIQUE,  -- SHA-256 of token
    user_id UUID REFERENCES users(id),
    telegram_user_id VARCHAR(50),
    wallet_address VARCHAR(42) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,  -- 'agent', 'mandate', 'portfolio'
    resource_id UUID,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP,
    INDEX idx_token_hash (token_hash),
    INDEX idx_expires_at (expires_at)
);
```

### Table: `user_sessions`
```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    session_token_hash VARCHAR(64) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    last_activity TIMESTAMP DEFAULT NOW(),
    user_agent TEXT,
    ip_address INET,
    INDEX idx_token_hash (session_token_hash),
    INDEX idx_user_id (user_id),
    INDEX idx_expires_at (expires_at)
);
```

### Table: `users` (additions)
```sql
ALTER TABLE users ADD COLUMN telegram_user_id VARCHAR(50) UNIQUE;
ALTER TABLE users ADD COLUMN telegram_username VARCHAR(100);
ALTER TABLE users ADD COLUMN last_telegram_sync TIMESTAMP;
```

---

## Security Considerations

### 1. Token Security
- ✅ Use HTTPS only for all deep links
- ✅ SHA-256 hash tokens before storing in database
- ✅ Short expiry times (5 min for deep links)
- ✅ Single-use tokens (mark as `used` after exchange)
- ✅ Rate limiting on token creation (max 10/minute per user)

### 2. Wallet Signature Verification
- ✅ Verify ECDSA signature matches wallet address
- ✅ Include nonce to prevent replay attacks
- ✅ Nonce must be fresh (< 5 minutes old)
- ✅ Store used nonces to prevent reuse

### 3. CSRF Protection
- ✅ SameSite cookies for session tokens
- ✅ CSRF tokens for state-changing operations
- ✅ Origin validation for API requests

### 4. Rate Limiting
- Deep link creation: 10/minute per user
- Token exchange: 20/minute per IP
- Wallet login: 5/minute per wallet address

---

## User Experience Patterns

### Pattern 1: First-Time Web User from Telegram

**Flow:**
1. User interacts with Telegram bot
2. Bot sends deep link: "View your dashboard →"
3. User clicks → Opens web app
4. Auto-authenticated via deep link token
5. Sees welcome modal:
   ```bash
   Welcome to Agent x402 Web! 🎉

   You're signed in with your wallet:
   0x742d...3bf8

   [Take a Tour] [Go to Dashboard]
   ```

### Pattern 2: Returning Web User

**Flow:**
1. User has existing session JWT in localStorage
2. Opens `app.agentx402.com`
3. App checks JWT validity
4. If valid: Auto-login to dashboard
5. If expired: Show "Connect Wallet" button

### Pattern 3: Expired Deep Link

**Flow:**
1. User clicks 10-minute-old Telegram deep link
2. Web app detects expired token
3. Shows friendly message:
   ```bash
   🔐 This link has expired for security

   No worries! You can still access your dashboard by:

   [Connect Wallet] [Return to Telegram]
   ```

---

## Implementation Phases

### Phase 1: Basic Deep Linking (Week 1) ✅
- [x] Create short-lived token endpoint
- [x] Token exchange endpoint
- [x] Web app auth token handler
- [x] Basic agent dashboard deep link

### Phase 2: Enhanced Context (Week 2)
- [ ] Add resource_id support (agents, mandates, trades)
- [ ] Implement token refresh mechanism
- [ ] Add session persistence
- [ ] Telegram notification webhooks

### Phase 3: Bi-Directional Flow (Week 3)
- [ ] Web → Telegram notifications
- [ ] Telegram Mini App integration
- [ ] Signature flow via Telegram
- [ ] QR code deep links

### Phase 4: Advanced Features (Week 4)
- [ ] Multi-device session management
- [ ] Session revocation UI
- [ ] Deep link analytics
- [ ] Smart fallback flows

---

## Error Handling

### Expired Token
```json
{
  "error": "token_expired",
  "message": "This link has expired. Please request a new one from Telegram.",
  "fallback_action": "connect_wallet"
}
```

### Invalid Token
```json
{
  "error": "invalid_token",
  "message": "This link is invalid or has already been used.",
  "fallback_action": "return_to_telegram"
}
```

### Resource Not Found
```json
{
  "error": "resource_not_found",
  "message": "The requested agent could not be found.",
  "fallback_action": "show_portfolio"
}
```

---

## Testing Strategy

### Unit Tests
- Token generation/validation
- Signature verification
- Nonce freshness checks

### Integration Tests
- End-to-end deep link flow
- Token exchange flow
- Session refresh flow

### E2E Tests
- Telegram bot → Web app transition
- Web app → Telegram notification
- Multi-device session handling

---

## Metrics & Monitoring

### Key Metrics
- Deep link click-through rate
- Token exchange success rate
- Average time from Telegram to Web
- Session duration
- Multi-platform user engagement

### Alerts
- High token exchange failure rate (> 10%)
- Unusual token creation volume
- Session hijacking attempts detected

---

## Future Enhancements

1. **QR Code Deep Links**
   - Generate QR codes in Telegram for mobile → desktop transitions

2. **Deep Link Previews**
   - Rich previews when sharing deep links in Telegram groups

3. **Universal Links (iOS) / App Links (Android)**
   - Native app deep linking support

4. **Cross-Chain Support**
   - Multi-wallet deep linking (Solana, Polygon, etc.)

5. **Analytics Dashboard**
   - Track user journey across platforms
   - Optimize conversion funnels

---

## Document Metadata

- **Version:** 1.0
- **Last Updated:** 2025-10-03
- **Status:** Draft → Implementation Ready
- **Related Documents:**
  - User Flows: Onboarding & Wallet Funding
  - Telegram Interaction Patterns
  - API Specification
