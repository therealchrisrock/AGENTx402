# Portfolio Management Flow - Agent x402

**Document ID**: PROJECT004
**Created By**: project-manager
**Created At**: 2025-10-03T08:10:42.645Z
**Project Root**: /Users/groot/Documents/code/telegram-402

---

# Portfolio Management Flow - Agent x402

## Overview

Portfolio management allows users to monitor active mandates, view performance, manage positions, and execute actions like extending, modifying, or closing mandates.

---

## Portfolio Overview Flow

```mermaid
flowchart TD
    Start([Entry: /portfolio]) --> LoadPortfolio[Load User Portfolio]

    LoadPortfolio --> HasMandates{Has active<br/>mandates?}

    HasMandates -->|No| EmptyPortfolio["No active mandates yet<br/><br/>[Create First Mandate]<br/>[Discover Strategies]"]

    HasMandates -->|Yes| DisplayPortfolio["📊 Your Portfolio<br/><br/>Total Value: $1,342.18 (+7.8%)<br/>Today's P&L: +$23.45 (+1.8%)<br/><br/>Active Mandates: 3"]

    DisplayPortfolio --> ShowMandates[Display Mandate List]

    ShowMandates --> MandateList["🟢 DCA Bot #M0001<br/>   $500 → $547.23 (+9.4%)<br/>   [Details] [Extend] [Close]<br/><br/>🟡 Grid Trading #M0002<br/>   $300 → $312.58 (+4.2%)<br/>   [Details] [Modify] [Close]<br/><br/>🔴 Arbitrage #M0003<br/>   $450 → $482.37 (+7.2%)<br/>   [Details] [Extend] [Close]"]

    MandateList --> Actions["[Create New Mandate]<br/>[Performance Analytics]"]

    Actions --> UserAction{User Action}

    UserAction -->|Details| PositionDetail[Position Detail View]
    UserAction -->|Extend| ExtendFlow[Mandate Renewal Flow]
    UserAction -->|Modify| ModifyFlow[Modify Settings Flow]
    UserAction -->|Close| CloseFlow[Close Position Flow]
    UserAction -->|Create New| CreateMandate[Mandate Creation]
    UserAction -->|Analytics| AnalyticsView[Analytics Dashboard]
    UserAction -->|NL Query| HandleNL[Natural Language Handler]

    PositionDetail --> MandateList
    ExtendFlow --> MandateList
    ModifyFlow --> MandateList
    CloseFlow --> MandateList
    AnalyticsView --> MandateList

    EmptyPortfolio --> CreateMandate

    style DisplayPortfolio fill:#e3f2fd
    style MandateList fill:#f3e5f5
    style EmptyPortfolio fill:#fff3e0
```

---

## Position Detail View

```mermaid
flowchart TD
    Entry([Select: Details]) --> LoadPosition[Load Position Data]

    LoadPosition --> DisplayDetail["DCA Bot #M0001<br/><br/>Status: Active 🟢<br/>Strategy: Dollar-cost averaging<br/>Risk: Moderate 🟡<br/><br/>Performance:<br/>Investment: $500.00<br/>Current: $547.23<br/>Profit: +$47.23 (+9.4%)<br/><br/>Duration:<br/>Created: Oct 1, 14:30<br/>Expires: Oct 8, 14:30 (2d 14h)<br/><br/>Recent Activity:<br/>• 2h ago: Bought 0.015 ETH @ $2,456<br/>• 8h ago: Bought 0.014 ETH @ $2,478"]

    DisplayDetail --> DetailActions["[Extend Mandate] [Add Funds]<br/>[Modify Risk] [Close Position]<br/>[← Back to Portfolio]"]

    DetailActions --> Action{User Action}

    Action -->|Extend| ExtendMandate[Extend Flow]
    Action -->|Add Funds| AddFunds[Add Funds Flow]
    Action -->|Modify Risk| ModifyRisk[Modify Risk Flow]
    Action -->|Close| ClosePosition[Close Flow]
    Action -->|Back| Portfolio[Portfolio Overview]
    Action -->|NL: extend for week| QuickExtend[Quick Extend]
    Action -->|NL: add $200| QuickAddFunds[Quick Add Funds]

    QuickExtend --> Confirm[Confirmation Dialog]
    QuickAddFunds --> Confirm

    Confirm --> Success[Action Complete]
    Success --> Portfolio

    style DisplayDetail fill:#e3f2fd
    style Success fill:#c8e6c9
```

---

## Mandate Renewal Flow

```mermaid
flowchart TD
    Start([Entry: Extend Mandate]) --> ShowCurrent["Current Mandate #M0001<br/><br/>Performance: +$47.23 (+9.4%)<br/>Expires: 2d 14h<br/><br/>Extend this mandate?"]

    ShowCurrent --> Options{Renewal Type}

    Options -->|Quick Renew| QuickRenew["Quick Renewal<br/><br/>Same settings:<br/>• $500 investment<br/>• DCA Bot<br/>• Moderate risk<br/><br/>New duration:<br/>[48 Hours] [1 Week] [1 Month]"]

    Options -->|Modify & Renew| ModifyRenew["Modify Before Renewal<br/><br/>What would you like to change?<br/><br/>[Amount] [Risk Level]<br/>[Duration] [Keep All]"]

    QuickRenew --> SelectDuration[Select Duration]
    SelectDuration --> ReviewRenewal

    ModifyRenew --> ChangeAmount{Change<br/>Amount?}
    ChangeAmount -->|Yes| NewAmount[Enter New Amount]
    ChangeAmount -->|No| ChangeRisk

    NewAmount --> ChangeRisk{Change<br/>Risk?}
    ChangeRisk -->|Yes| NewRisk[Select New Risk]
    ChangeRisk -->|No| ChangeDuration

    NewRisk --> ChangeDuration{Change<br/>Duration?}
    ChangeDuration -->|Yes| NewDuration[Select Duration]
    ChangeDuration -->|No| ReviewRenewal

    NewDuration --> ReviewRenewal

    ReviewRenewal["Review Renewal<br/><br/>Original:<br/>• $500, Moderate, 7d<br/>• Earned: +$47.23<br/><br/>New Terms:<br/>• $700, Moderate, 14d<br/>• Est: $8-18 (1.1-2.6%)<br/><br/>[✅ Confirm Renewal] [Cancel]"] --> ConfirmRenew{Confirm?}

    ConfirmRenew -->|Yes| SignatureReq[Request Signature]
    ConfirmRenew -->|No| Start

    SignatureReq --> WaitSign[Wait for Wallet]

    WaitSign --> SignResult{Result}

    SignResult -->|Approved| RenewSuccess["✅ Mandate Renewed!<br/><br/>New expiry: Oct 22, 14:30<br/><br/>[View Position] [Back to Portfolio]"]
    SignResult -->|Rejected| SignError["❌ Renewal failed<br/><br/>[Retry] [Cancel]"]

    SignError --> RetrySign{Retry?}
    RetrySign -->|Yes| SignatureReq
    RetrySign -->|No| Start

    RenewSuccess --> End([Complete])

    style ReviewRenewal fill:#fff3e0
    style RenewSuccess fill:#c8e6c9
    style SignError fill:#ffcdd2
```

---

## Close Position Flow

```mermaid
flowchart TD
    Start([Entry: Close Position]) --> ShowPosition["Close DCA Bot #M0001?<br/><br/>Current Status:<br/>• Investment: $500<br/>• Current Value: $547.23<br/>• Profit: +$47.23 (+9.4%)<br/><br/>⚠️ This will stop trading and<br/>return funds to your wallet"]

    ShowPosition --> CloseOptions{Close Method}

    CloseOptions -->|Market Close| MarketClose["Immediate Close<br/><br/>• Close all positions now<br/>• At current market prices<br/>• Funds available immediately<br/><br/>[Confirm Market Close]"]

    CloseOptions -->|Smart Close| SmartClose["Smart Close (AI Optimized)<br/><br/>• Wait for optimal prices<br/>• Max wait: 24 hours<br/>• Better execution likely<br/><br/>[Confirm Smart Close]"]

    CloseOptions -->|Cancel| Back[Back to Portfolio]

    MarketClose --> ConfirmMarket{Confirm?}
    SmartClose --> ConfirmSmart{Confirm?}

    ConfirmMarket -->|Yes| ExecuteMarket[Execute Market Close]
    ConfirmMarket -->|No| Start

    ConfirmSmart -->|Yes| ExecuteSmart[Queue Smart Close]
    ConfirmSmart -->|No| Start

    ExecuteMarket --> Processing["⏳ Closing positions...<br/><br/>Please wait..."]

    Processing --> CloseResult{Result}

    CloseResult -->|Success| CloseSuccess["✅ Position Closed<br/><br/>Final Value: $547.23<br/>Total Profit: +$47.23 (+9.4%)<br/>Funds returned to wallet<br/><br/>[View Transaction]<br/>[Create New Mandate]<br/>[Back to Portfolio]"]

    CloseResult -->|Error| CloseError["❌ Close failed<br/><br/>Positions still active<br/><br/>[Retry] [Contact Support]"]

    ExecuteSmart --> SmartQueued["✅ Smart Close Queued<br/><br/>Your position will close when<br/>optimal prices are reached<br/><br/>Max wait: 24 hours<br/><br/>[Monitor Progress]<br/>[Cancel Smart Close]<br/>[Back to Portfolio]"]

    CloseSuccess --> End([Complete])
    CloseError --> Retry{Retry?}
    Retry -->|Yes| Start
    Retry -->|No| Back

    SmartQueued --> End

    style CloseSuccess fill:#c8e6c9
    style CloseError fill:#ffcdd2
    style Processing fill:#fff3e0
    style SmartQueued fill:#e3f2fd
```

---

## Performance Analytics

```mermaid
flowchart TD
    Start([Entry: Performance Analytics]) --> LoadData[Load Portfolio History]

    LoadData --> SelectPeriod["Select Time Period<br/><br/>[24 Hours] [7 Days] [30 Days] [All Time]<br/><br/>Current: 30 Days"]

    SelectPeriod --> DisplayAnalytics["📊 Performance Analytics (30d)<br/><br/>Total Return: +$127.45 (+10.2%)<br/>Win Rate: 68%<br/>Best Day: +$45.23 (Oct 15)<br/>Worst Day: -$12.50 (Oct 8)<br/><br/>By Strategy:<br/>🟢 DCA: +9.4% (3 mandates)<br/>🟡 Grid: +8.7% (2 mandates)<br/>🔴 Arb: +12.1% (1 mandate)"]

    DisplayAnalytics --> AnalyticsActions["[View Chart] [Export Data]<br/>[Risk Metrics] [Compare Strategies]<br/>[��� Back]"]

    AnalyticsActions --> Action{User Action}

    Action -->|View Chart| ShowChart[Display Performance Chart]
    Action -->|Export| ExportFlow[Export Data Flow]
    Action -->|Risk Metrics| RiskView[Risk Metrics Dashboard]
    Action -->|Compare| CompareView[Strategy Comparison]
    Action -->|Back| Portfolio[Portfolio Overview]

    ShowChart --> ChartDisplay["📈 Performance Chart<br/><br/>[Line chart visualization]<br/><br/>• Portfolio value over time<br/>• Individual strategy lines<br/>• Benchmark comparison<br/><br/>[Download Chart] [← Back]"]

    ChartDisplay --> AnalyticsActions

    ExportFlow --> ExportOptions["Export Format:<br/><br/>[CSV] [JSON] [PDF Report]"]

    ExportOptions --> GenerateExport[Generate File]
    GenerateExport --> SendFile["✅ File ready!<br/><br/>📎 portfolio_30d.csv<br/><br/>[Download] [← Back]"]

    SendFile --> AnalyticsActions

    RiskView --> RiskDisplay["⚠️ Risk Metrics<br/><br/>Sharpe Ratio: 2.8<br/>Max Drawdown: 3.2%<br/>Volatility: 12.5%<br/>Beta: 0.85<br/><br/>Risk Level: Moderate 🟡<br/><br/>[← Back]"]

    RiskDisplay --> AnalyticsActions

    CompareView --> CompareDisplay["Strategy Comparison<br/><br/>DCA vs Grid vs Arbitrage<br/><br/>Returns: 9.4% | 8.7% | 12.1%<br/>Risk: Low | Med | High<br/>Win Rate: 78% | 65% | 58%<br/><br/>[← Back]"]

    CompareDisplay --> AnalyticsActions

    style DisplayAnalytics fill:#e3f2fd
    style ChartDisplay fill:#f3e5f5
    style SendFile fill:#c8e6c9
```

---

## Natural Language Queries

### Portfolio Queries

```mermaid
flowchart LR
    Query["User Query"] --> Parse[Intent Classification]

    Parse --> Intent{Intent Type}

    Intent -->|Status| Status["Show portfolio status<br/>+ quick actions"]
    Intent -->|Performance| Perf["Show performance metrics<br/>+ analytics link"]
    Intent -->|Specific Bot| Bot["Show bot details<br/>+ actions"]
    Intent -->|Close| Close["Initiate close flow<br/>+ confirmation"]
    Intent -->|Modify| Modify["Show modification options<br/>+ parameters"]

    Status --> Response[Send Response]
    Perf --> Response
    Bot --> Response
    Close --> Response
    Modify --> Response
```

### Example Queries & Responses

**"How is my portfolio doing?"**
```
📊 Your Portfolio Performance

Total Value: $1,342.18 (+7.8%)
Today: +$23.45 (+1.8%) 🟢

Active Mandates: 3
All performing well!

[View Details] [Performance Analytics]
```

**"Close my DCA position"**
```
You want to close DCA Bot #M0001?

Current Status:
• Investment: $500
• Current Value: $547.23
• Profit: +$47.23 (+9.4%)

[Close Now] [Smart Close] [Cancel]
```

**"How is my arbitrage bot doing?"**
```
Arbitrage #M0003 Status:

• Investment: $450
• Current: $482.37
• Profit: +$32.37 (+7.2%)
• Status: Active 🔴
• Expires: 12 hours

Recent trades:
• 30m ago: +$2.15 (Arb ETH/USDC)
• 2h ago: +$1.87 (Arb BTC/USDC)

[View Full Details] [Extend] [Close]
```

**"Add $200 to Grid Trading"**
```
Add $200 to Grid Trading #M0002?

Current: $300 → $312.58 (+4.2%)
New Total: $500

This will:
• Increase position size
• Require new signature
• Keep same risk/duration

[Confirm] [Change Amount] [Cancel]
```

---

## Entry Methods

### Commands
- `/portfolio` or `/positions` - Main portfolio view
- `/stats` - Quick statistics
- `/close <mandate_id>` - Close specific mandate

### Natural Language
- "Show my portfolio"
- "How are my investments doing?"
- "Close my DCA position"
- "Extend arbitrage for another week"
- "Add $200 to grid trading"

### Buttons
- `[Portfolio]` from main menu
- `[View Position]` from notifications
- `[Back to Portfolio]` from detail views

---

## State Management

### Portfolio State
```javascript
{
  userId: "123456789",
  activeMandates: [
    {
      id: "M0001",
      strategy: "dca",
      amount: 500,
      currentValue: 547.23,
      pnl: 47.23,
      pnlPercent: 9.4,
      status: "ACTIVE",
      expiresAt: "2025-10-08T14:30:00Z"
    }
  ],
  totalValue: 1342.18,
  totalPnl: 127.45,
  totalPnlPercent: 10.2
}
```

### Position Detail State
```javascript
{
  mandateId: "M0001",
  viewType: "DETAIL",
  activeTab: "performance",  // performance | history | settings
  refreshInterval: 30000     // Auto-refresh every 30s
}
```

---

## Auto-Refresh & Real-time Updates

### Refresh Strategy
- **Portfolio Overview**: Refresh every 30 seconds
- **Position Detail**: Refresh every 10 seconds
- **Active Close**: Refresh every 5 seconds
- **Smart Close Queue**: Refresh every 60 seconds

### Real-time Events
```mermaid
flowchart LR
    Event[Blockchain Event] --> Webhook[Webhook Handler]
    Webhook --> Classify{Event Type}

    Classify -->|Trade Executed| TradeNotif[Trade Notification]
    Classify -->|Position Updated| UpdatePortfolio[Update Portfolio Cache]
    Classify -->|Mandate Expired| ExpiryNotif[Expiry Notification]

    TradeNotif --> SendUser[Send to User]
    UpdatePortfolio --> SendUser
    ExpiryNotif --> SendUser

    SendUser --> UserRefresh[Auto-refresh UI]
```

---

## Message Templates

### Portfolio Overview
```
📊 Your Portfolio

Total Value: $1,342.18 (+7.8%)
Today: +$23.45 (+1.8%) 🟢

Active Mandates: 3

🟢 DCA Bot #M0001
   $500 → $547.23 (+9.4%)
   Expires: 2d 14h
   [Details] [Extend] [Close]

🟡 Grid Trading #M0002
   $300 → $312.58 (+4.2%)
   Expires: 5d 3h
   [Details] [Modify] [Close]

🔴 Arbitrage #M0003
   $450 → $482.37 (+7.2%)
   Expires: 12h
   [Details] [Extend] [Close]

[Create New Mandate] [Performance Analytics]
```

### Position Detail
```
DCA Bot #M0001

Status: Active 🟢
Strategy: Dollar-cost averaging
Risk: Moderate 🟡

Performance:
Investment: $500.00
Current: $547.23
Profit: +$47.23 (+9.4%)

Duration:
Created: Oct 1, 14:30
Expires: Oct 8, 14:30 (2d 14h)

Recent Activity:
• 2h ago: Bought 0.015 ETH @ $2,456
• 8h ago: Bought 0.014 ETH @ $2,478
• 1d ago: Bought 0.016 ETH @ $2,443

[Extend Mandate] [Add Funds] [Modify Risk]
[Close Position] [← Back to Portfolio]
```

### Empty Portfolio
```
No active mandates yet

Ready to start trading?

[Create First Mandate] [Discover Strategies]
[Learn About Mandates]
```

---

## Success Metrics

### Portfolio Engagement
- Daily portfolio views
- Average time in portfolio view
- Actions per session

### Position Management
- Renewal rate
- Average mandate duration
- Close reasons distribution

### Performance Tracking
- Analytics view rate
- Export frequency
- Chart interaction rate