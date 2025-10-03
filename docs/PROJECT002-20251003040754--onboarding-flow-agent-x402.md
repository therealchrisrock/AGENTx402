# Onboarding Flow - Agent x402

**Document ID**: PROJECT002
**Created By**: project-manager
**Created At**: 2025-10-03T08:07:54.684Z
**Project Root**: /Users/groot/Documents/code/telegram-402

---

# Onboarding Flow - Agent x402

## Overview

Phase 1 onboarding focuses on direct wallet connection (Option A: User Custody). Users connect their existing wallet, and the bot checks their balance to determine next steps.

---

## User States

```mermaid
stateDiagram-v2
    [*] --> NEW_USER: First /start
    NEW_USER --> WALLET_CONNECTED_NO_FUNDS: Wallet connected, balance < $50
    NEW_USER --> WALLET_CONNECTED_FUNDED: Wallet connected, balance >= $50

    WALLET_CONNECTED_NO_FUNDS --> WALLET_CONNECTED_FUNDED: Funds added

    WALLET_CONNECTED_FUNDED --> ACTIVE_TRADER: First mandate created

    note right of WALLET_CONNECTED_NO_FUNDS
        Can browse strategies
        Can plan investments
        Cannot create mandates
    end note

    note right of WALLET_CONNECTED_FUNDED
        Full platform access
        Can create mandates
        Can trade
    end note
```

---

## Complete Onboarding Flow

```mermaid
flowchart TD
    Start([User: /start]) --> CheckUser{Returning<br/>user?}

    CheckUser -->|Yes| Dashboard[Show Main Dashboard]
    CheckUser -->|No| Welcome[Welcome Message]

    Welcome --> ConnectPrompt["👋 Welcome to Agent x402!<br/><br/>Connect your wallet to get started<br/><br/>[Connect Wallet] [What is this?]"]

    ConnectPrompt -->|Button: What is this?| Educational[Educational Content]
    Educational --> ConnectPrompt

    ConnectPrompt -->|Button: Connect Wallet| WalletOptions["Choose wallet type:<br/><br/>[MetaMask] [WalletConnect]<br/>[Phantom] [Manual Entry]"]

    WalletOptions -->|MetaMask| MetaMaskFlow[Mini App Integration]
    WalletOptions -->|WalletConnect| WCFlow[WalletConnect Integration]
    WalletOptions -->|Phantom| PhantomFlow[Phantom Integration]
    WalletOptions -->|Manual Entry| ManualInput[Enter Wallet Address]

    ManualInput --> ValidateAddress{Valid<br/>address?}
    ValidateAddress -->|No| ErrorMessage["❌ Invalid address<br/><br/>Format: 0x...<br/><br/>[Try Again] [Cancel]"]
    ErrorMessage --> ManualInput

    ValidateAddress -->|Yes| WalletConnected
    MetaMaskFlow -->|Success| WalletConnected
    WCFlow -->|Success| WalletConnected
    PhantomFlow -->|Success| WalletConnected

    WalletConnected["✅ Wallet Connected!<br/>Address: 0x742d...3bf8"] --> CheckBalance[Check Wallet Balance]

    CheckBalance --> HasFunds{Balance<br/>>= $50?}

    HasFunds -->|Yes| FundedWelcome["✅ Balance: $1,245.50 USDC<br/><br/>You're ready to trade!<br/><br/>[Create First Mandate]<br/>[Explore Strategies]"]

    HasFunds -->|No| NoFunds["Balance: $0 USDC<br/><br/>No funds yet, but you can:<br/><br/>[💰 How to Add Funds]<br/>[🔍 Browse Strategies]"]

    NoFunds -->|Browse| BrowseStrategies[Strategy Discovery]
    NoFunds -->|How to Add Funds| FundingGuide[Funding Instructions]

    FundingGuide --> WaitFunds{Funds<br/>added?}
    WaitFunds -->|Yes| FundedWelcome
    WaitFunds -->|No| NoFunds

    FundedWelcome -->|Create Mandate| MandateFlow[Mandate Creation Flow]
    FundedWelcome -->|Explore| BrowseStrategies

    BrowseStrategies --> Dashboard
    MandateFlow --> Dashboard

    Dashboard --> End([Onboarding Complete])

    style WalletConnected fill:#c8e6c9
    style FundedWelcome fill:#c8e6c9
    style NoFunds fill:#fff3e0
    style ErrorMessage fill:#ffcdd2
```

---

## Interaction Methods

### Commands
- `/start` - Entry point for new users
- `/wallet` - Access wallet management (during onboarding)
- `/help` - Context-sensitive help

### Natural Language
- "I want to learn first" → Educational content
- "I'll use MetaMask" → MetaMask flow
- "I'll add funds later" → Skip to dashboard

### Buttons
**Step 1 - Welcome:**
- `[Connect Wallet]` - Start connection flow
- `[What is this?]` - Educational overlay

**Step 2 - Wallet Selection:**
- `[MetaMask]` - MetaMask integration
- `[WalletConnect]` - WalletConnect integration
- `[Phantom]` - Phantom integration
- `[Manual Entry]` - Manual address input

**Step 3 - Post-Connection:**
- Funded: `[Create First Mandate]` `[Explore Strategies]`
- Empty: `[How to Add Funds]` `[Browse Strategies]`

---

## Message Templates

### Welcome (New User)
```
Welcome to Agent x402! 🤖

Your AI-powered trading assistant for autonomous crypto strategies.

Let's connect your wallet to get started.

[Connect Wallet] [What is this?]
```

### Wallet Selection
```
Choose your wallet type:

[MetaMask] [WalletConnect]
[Phantom] [Manual Entry]

[← Back]
```

### Manual Address Input
```
Enter your wallet address:

Format: 0x followed by 40 characters

[Cancel]
```

### Wallet Connected - Funded
```
✅ Wallet connected!
Address: 0x742d...3bf8

Balance: 1,245.50 USDC

You're ready to trade!

[Create First Mandate] [Explore Strategies]
```

### Wallet Connected - Empty
```
✅ Wallet connected!
Address: 0x742d...3bf8

Balance: 0 USDC

No funds yet, but you can:
[💰 How to Add Funds] [🔍 Browse Strategies]
```

### Invalid Address Error
```
❌ Invalid wallet address

Please enter a valid Ethereum address:
Format: 0x followed by 40 characters

[Try Again] [Cancel]
```

---

## State Management

### User State Schema
```javascript
{
  userId: "123456789",
  accountState: "WALLET_CONNECTED_FUNDED",
  walletAddress: "0x742d35e9...",
  balance: {
    usdc: 1245.50,
    eth: 0.15
  },
  onboardingComplete: true,
  onboardedAt: "2025-10-03T10:30:00Z"
}
```

### Flow Context (During Onboarding)
```javascript
{
  activeFlow: {
    flowType: "ONBOARDING",
    currentStep: 2,
    stepName: "WALLET_SELECTION",
    startedAt: "2025-10-03T10:30:00Z"
  }
}
```

---

## Error Handling

### Wallet Connection Failed
```mermaid
flowchart TD
    Error[Connection Failed] --> Classify{Error Type}

    Classify -->|User Rejected| Rejected["❌ Connection declined<br/><br/>[Retry] [Try Different Wallet]"]
    Classify -->|Network Error| Network["⚠️ Connection issue<br/><br/>[Retry] [Check Network]"]
    Classify -->|Unsupported Wallet| Unsupported["❌ Wallet not supported<br/><br/>[Try Another] [Manual Entry]"]

    Rejected --> Retry{User Action}
    Network --> Retry
    Unsupported --> Manual[Manual Entry Flow]

    Retry -->|Retry| Attempt[Retry Connection]
    Retry -->|Different| WalletSelect[Wallet Selection]
    Retry -->|Cancel| Cancel[Return to Welcome]
```

### Invalid Address Input
- Validate format: `^0x[a-fA-F0-9]{40}$`
- Show error with example
- Allow retry or cancel

### Balance Check Failed
- Retry with exponential backoff
- Fallback: Allow manual balance entry
- Show warning if balance cannot be verified

---

## Success Criteria

### Onboarding Complete When:
1. ✅ Wallet connected successfully
2. ✅ Address validated and saved
3. ✅ Balance checked (or manual confirmation)
4. ✅ User reaches main dashboard

### Metrics to Track:
- Time to wallet connection
- Wallet connection success rate
- Funding conversion rate (empty → funded)
- Onboarding abandonment by step

---

## Phase 1 Simplifications

### Removed Features (for Phase 1):
- ❌ Demo mode / paper trading
- ❌ Testnet mode
- ❌ Email/phone registration
- ❌ Social login options
- ❌ Wallet creation (users must have existing wallet)

### Future Enhancements:
- 🔮 Demo mode for practice
- 🔮 Fiat on-ramp integration
- 🔮 Multi-wallet support
- 🔮 Wallet creation for new users
- 🔮 Social recovery options