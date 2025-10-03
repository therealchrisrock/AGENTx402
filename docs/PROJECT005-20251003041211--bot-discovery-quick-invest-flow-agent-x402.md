# Bot Discovery & Quick Invest Flow - Agent x402

**Document ID**: PROJECT005
**Created By**: project-manager
**Created At**: 2025-10-03T08:12:11.001Z
**Project Root**: /Users/groot/Documents/code/telegram-402

---

# Bot Discovery & Quick Invest Flow - Agent x402

## Overview

The discovery flow allows users to browse available trading strategies, compare performance, and quickly invest in bots with pre-configured optimal settings.

---

## Discovery Flow

```mermaid
flowchart TD
    Start([Entry Point]) --> EntryType{Entry Method}

    EntryType -->|/discover command| MainDiscover
    EntryType -->|Button: Discover| MainDiscover
    EntryType -->|NL: show me bots| MainDiscover

    MainDiscover[Load Strategy List] --> DisplayStrategies["🔍 Top Trading Strategies<br/><br/>Filter by:<br/>[🏆 Top Gainers] [🛡️ Conservative]<br/>[⚡ Aggressive] [📈 Long-term]"]

    DisplayStrategies --> StrategyList["1. 🥇 Conservative DCA Bot<br/>   APY: 12.5% | Risk: Low 🟢<br/>   Min: $50 | 1,234 users<br/>   [Quick Invest] [Details]<br/><br/>2. 🥈 Grid Trading Pro<br/>   APY: 18.3% | Risk: Medium 🟡<br/>   Min: $100 | 856 users<br/>   [Quick Invest] [Details]<br/><br/>3. 🥉 Arbitrage Master<br/>   APY: 24.7% | Risk: High 🔴<br/>   Min: $200 | 432 users<br/>   [Quick Invest] [Details]"]

    StrategyList --> Actions{User Action}

    Actions -->|Filter| ApplyFilter[Apply Filter]
    Actions -->|Quick Invest| QuickInvest[Quick Invest Flow]
    Actions -->|Details| BotDetail[Bot Detail View]
    Actions -->|NL: best for beginners| FilterRecommend[Filter + Recommend]
    Actions -->|Load More| LoadMore[Load Next Page]

    ApplyFilter --> DisplayStrategies

    FilterRecommend --> Recommend["Based on 'beginners', I recommend:<br/><br/>🛡️ Conservative DCA Bot<br/>• Low risk, steady returns<br/>• Perfect for learning<br/>• $50 minimum<br/><br/>[Quick Invest] [See More]"]

    Recommend --> Actions

    LoadMore --> StrategyList

    BotDetail --> DetailFlow[Bot Detail Flow]
    QuickInvest --> InvestFlow[Quick Invest Flow]

    DetailFlow --> Actions
    InvestFlow --> Complete([Investment Complete])

    style DisplayStrategies fill:#e3f2fd
    style Recommend fill:#c8e6c9
```

---

## Bot Detail View

```mermaid
flowchart TD
    Start([Entry: Details]) --> LoadBot[Load Bot Data]

    LoadBot --> DisplayDetail["🛡️ Conservative DCA Bot<br/><br/>Strategy: Dollar-cost averaging<br/>Risk: Low 🟢 | Min: $50<br/><br/>Performance:<br/>• 30d: +12.5%<br/>• 90d: +38.7%<br/>• All-time: +127.3%<br/><br/>Risk Metrics:<br/>• Max Drawdown: 3.2%<br/>• Sharpe Ratio: 2.8<br/>• Win Rate: 78%<br/><br/>Active Users: 1,234<br/>Total Value Locked: $2.3M"]

    DisplayDetail --> DetailActions["[Quick Invest] [Add to Watchlist]<br/>[Compare with Others] [View Strategy]<br/>[← Back to Discovery]"]

    DetailActions --> Action{User Action}

    Action -->|Quick Invest| QuickInvest[Quick Invest Flow]
    Action -->|Watchlist| AddWatch[Add to Watchlist]
    Action -->|Compare| CompareFlow[Comparison Mode]
    Action -->|View Strategy| StrategyInfo[Strategy Explanation]
    Action -->|Back| Discovery[Discovery View]
    Action -->|NL: invest $500| PreFillInvest["Pre-fill amount<br/>→ Quick Invest"]

    AddWatch --> WatchConfirm["✅ Added to Watchlist<br/><br/>[Set Alert] [← Back]"]
    WatchConfirm --> DetailActions

    StrategyInfo --> InfoDisplay["📚 DCA Strategy Explained<br/><br/>Dollar-Cost Averaging invests<br/>fixed amounts at regular intervals<br/><br/>Benefits:<br/>• Reduces timing risk<br/>• Averages entry price<br/>• Lower volatility<br/><br/>Best for:<br/>• Long-term investing<br/>• Risk-averse users<br/><br/>[← Back]"]

    InfoDisplay --> DetailActions

    QuickInvest --> InvestComplete
    PreFillInvest --> InvestComplete
    CompareFlow --> Discovery

    InvestComplete([Investment Flow])

    style DisplayDetail fill:#e3f2fd
    style WatchConfirm fill:#c8e6c9
```

---

## Comparison Mode

```mermaid
flowchart TD
    Start([Select: Compare]) --> SelectBots["Select bots to compare<br/>(max 3)<br/><br/>☑️ Conservative DCA Bot<br/>☐ Grid Trading Pro<br/>☐ Arbitrage Master<br/><br/>[Compare Selected] [Cancel]"]

    SelectBots --> Selected{Bots<br/>Selected}

    Selected -->|< 2| Warning["⚠️ Select at least 2 bots"]
    Selected -->|2-3| ShowComparison

    Warning --> SelectBots

    ShowComparison["📊 Strategy Comparison<br/><br/>━━━━━━━━━━━━━━━━━━━━━━━━<br/>         DCA | Grid | Arbitrage<br/>━━━━━━━━━━━━━━━━━━━━━━━━<br/>APY:     12.5% | 18.3% | 24.7%<br/>Risk:    Low   | Med   | High<br/>Min:     $50   | $100  | $200<br/>Win Rate: 78%   | 65%   | 58%<br/>Users:   1,234 | 856   | 432<br/>━━━━━━━━━━━━━━━━━━━━━━━━<br/><br/>Best for you: Conservative DCA<br/>(Based on your risk profile)"]

    ShowComparison --> CompareActions["[Invest in DCA] [Invest in Grid]<br/>[Invest in Arbitrage] [← Back]"]

    CompareActions --> Action{User Action}

    Action -->|Invest in X| QuickInvest[Quick Invest Flow]
    Action -->|Back| Discovery[Discovery View]

    QuickInvest --> Complete([Investment Complete])

    style ShowComparison fill:#e3f2fd
    style CompareActions fill:#f3e5f5
```

---

## Quick Invest Flow

```mermaid
flowchart TD
    Start([Entry: Quick Invest]) --> PreConfig["Quick Invest: Conservative DCA Bot<br/><br/>✅ Optimal settings pre-configured!<br/><br/>Amount:<br/>Available: $1,245.50<br/>Recommended: $100-500"]

    PreConfig --> AmountSelect["[$100] [$250] [$500] [Custom]"]

    AmountSelect --> AmountInput{Amount}

    AmountInput -->|Button: $500| ValidAmount1
    AmountInput -->|Custom| CustomAmount[Enter Amount]

    CustomAmount --> ValidAmount1{Valid?}

    ValidAmount1 -->|No| AmountError["❌ Invalid amount<br/><br/>[Try Again]"]
    ValidAmount1 -->|Yes| SaveAmount[Save: amount = $500]

    AmountError --> AmountSelect

    SaveAmount --> DurationSelect["Duration:<br/><br/>[1 Week] [1 Month] [Custom]"]

    DurationSelect --> DurationInput{Duration}

    DurationInput -->|Button: 1 Week| SaveDuration[Save: duration = 7d]
    DurationInput -->|Custom| CustomDuration[Enter Duration]

    CustomDuration --> SaveDuration

    SaveDuration --> RiskConfig["Risk: Moderate 🟡 (Recommended)<br/><br/>Keep recommended or change?<br/><br/>[Keep Moderate] [Change Risk]"]

    RiskConfig --> RiskChoice{Choice}

    RiskChoice -->|Keep| SaveRisk[Save: risk = moderate]
    RiskChoice -->|Change| SelectRisk[Risk Selection]

    SelectRisk --> SaveRisk

    SaveRisk --> QuickReview["Quick Review<br/><br/>Conservative DCA Bot<br/>• Amount: $500<br/>• Duration: 1 week<br/>• Risk: Moderate 🟡<br/><br/>Expected: $5.77-$13.46<br/>Fees: ~$2.50<br/><br/>[✅ Confirm & Sign] [Cancel]"]

    QuickReview --> ReviewAction{Action}

    ReviewAction -->|Confirm| Signature[Signature Request]
    ReviewAction -->|Cancel| Cancel[Return to Discovery]

    Signature --> WaitSign[Wait for Wallet]

    WaitSign --> SignResult{Result}

    SignResult -->|Approved| Success["✅ Investment Successful!<br/><br/>Mandate #M0004 created<br/>Conservative DCA Bot trading<br/><br/>[View Position] [Discover More]"]
    SignResult -->|Rejected| SignError["❌ Signature rejected<br/><br/>[Retry] [Cancel]"]

    SignError --> RetrySign{Retry?}
    RetrySign -->|Yes| Signature
    RetrySign -->|No| Cancel

    Success --> Complete([Complete])

    style PreConfig fill:#e3f2fd
    style QuickReview fill:#fff3e0
    style Success fill:#c8e6c9
    style SignError fill:#ffcdd2
```

---

## Filter System

### Available Filters

```mermaid
flowchart LR
    Filters[Filter Options] --> Performance[Performance Filters]
    Filters --> Risk[Risk Filters]
    Filters --> Strategy[Strategy Filters]
    Filters --> Investment[Investment Filters]
    Filters --> Time[Timeframe Filters]

    Performance --> TopGain["🏆 Top Gainers"]
    Performance --> Consistent["📊 Most Consistent"]
    Performance --> Recent["🔥 Hot This Week"]

    Risk --> Conservative["🛡️ Conservative"]
    Risk --> Moderate["⚖️ Moderate"]
    Risk --> Aggressive["⚡ Aggressive"]

    Strategy --> DCA["DCA Bots"]
    Strategy --> Grid["Grid Trading"]
    Strategy --> Arb["Arbitrage"]

    Investment --> Small["< $100"]
    Investment --> Medium["$100-500"]
    Investment --> Large["> $500"]

    Time --> Short["⏱️ Short-term"]
    Time --> Long["📈 Long-term"]
```

### Filter Combinations

**Example 1: Conservative + Top Gainers**
```
🛡️ Conservative Top Gainers

1. Conservative DCA Bot
   APY: 12.5% | Risk: Low 🟢
   [Quick Invest] [Details]

2. Safe Grid Trading
   APY: 10.8% | Risk: Low 🟢
   [Quick Invest] [Details]

[Clear Filters] [Add More Filters]
```

**Example 2: < $100 + Short-term**
```
💰 Affordable Short-term Strategies

1. Quick DCA (48h cycles)
   Min: $50 | APY: 8.5%
   [Quick Invest] [Details]

2. Fast Grid (24h cycles)
   Min: $75 | APY: 11.2%
   [Quick Invest] [Details]

[Clear Filters] [Add More Filters]
```

---

## Natural Language Discovery

### Query Processing

```mermaid
flowchart TD
    Query["User: Show me safe strategies"] --> Parse[Parse Intent]

    Parse --> Extract[Extract Criteria]

    Extract --> Criteria{Criteria Type}

    Criteria -->|Risk Level| RiskFilter["Filter: risk = low<br/>Keyword: 'safe'"]
    Criteria -->|Performance| PerfFilter["Filter: top performing"]
    Criteria -->|Strategy Type| StratFilter["Filter: strategy = dca"]
    Criteria -->|Budget| BudgetFilter["Filter: min <= budget"]

    RiskFilter --> ApplyFilters
    PerfFilter --> ApplyFilters
    StratFilter --> ApplyFilters
    BudgetFilter --> ApplyFilters

    ApplyFilters[Apply All Filters] --> Results[Generate Results]

    Results --> Display["Show filtered bots<br/>+ Explanation"]

    Display --> Recommend{AI<br/>Recommend?}

    Recommend -->|Yes| ShowTop["Highlight top recommendation"]
    Recommend -->|No| ShowAll["Show all matches"]

    ShowTop --> Actions[Quick Actions]
    ShowAll --> Actions

    Actions --> User[Send to User]
```

### Example NL Queries

**"Show me the best bot for beginners"**
```
Based on "beginners", I recommend:

🛡️ Conservative DCA Bot

• Perfect for learning
• Low risk, steady returns
• $50 minimum
• 78% win rate

Why this is best for you:
✅ Simple strategy
✅ Proven track record
✅ Low entry barrier
✅ Strong risk management

[Quick Invest $100] [Learn More] [See Others]
```

**"Find me high-return strategies under $200"**
```
High-Return Strategies (< $200):

1. ⚡ Arbitrage Master
   APY: 24.7% | Min: $150
   Risk: High 🔴
   [Quick Invest] [Details]

2. 📈 Aggressive Grid
   APY: 21.3% | Min: $100
   Risk: High 🔴
   [Quick Invest] [Details]

⚠️ Note: Higher returns = higher risk
Consider starting small.

[Invest] [Show Conservative Options]
```

**"What's performing well this week?"**
```
🔥 Hot This Week

1. 🥇 Grid Trading Pro
   7d: +8.2% | APY: 18.3%
   [Quick Invest] [Details]

2. 🥈 DCA Bot Advanced
   7d: +6.7% | APY: 15.1%
   [Quick Invest] [Details]

3. 🥉 Arbitrage Lite
   7d: +9.4% | APY: 22.8%
   [Quick Invest] [Details]

[Invest in Top Pick] [See All Strategies]
```

---

## Watchlist Management

### Add to Watchlist

```mermaid
flowchart TD
    Start([Add to Watchlist]) --> AddItem[Add Bot to Watchlist]

    AddItem --> SetAlert{Set<br/>Alert?}

    SetAlert -->|Yes| AlertType["Alert Type:<br/><br/>[Price Target] [Performance]<br/>[Availability] [New Version]"]

    SetAlert -->|No| Confirm

    AlertType --> AlertConfig[Configure Alert]

    AlertConfig --> Confirm["✅ Added to Watchlist<br/><br/>Conservative DCA Bot<br/><br/>Alert: Notify when APY > 15%<br/><br/>[View Watchlist] [← Back]"]

    Confirm --> Complete([Complete])

    style Confirm fill:#c8e6c9
```

### View Watchlist

```
⭐ Your Watchlist

1. Conservative DCA Bot
   Current APY: 12.5%
   Alert: When APY > 15%
   [Quick Invest] [Remove]

2. Grid Trading Pro
   Current APY: 18.3%
   Alert: When available < $75
   [Quick Invest] [Remove]

[Set New Alert] [Clear Watchlist]
```

---

## Entry Methods

### Commands
- `/discover` or `/top` or `/bots` - Browse strategies
- `/compare <bot1> <bot2>` - Compare specific bots

### Natural Language
- "Show me top performing bots"
- "What's the best strategy for beginners?"
- "I want to try arbitrage"
- "Find me low-risk options under $100"

### Buttons
- `[Discover Strategies]` from main menu
- `[Quick Invest]` from bot card
- `[Details]` from bot card

---

## Bot Card Information

### Display Format
```
🥇 Conservative DCA Bot
   APY: 12.5% | Risk: Low 🟢
   Min: $50 | 1,234 users
   [Quick Invest] [Details]
```

### Data Shown
- **Rank**: Position in current filter
- **Name**: Bot strategy name
- **APY**: Annualized return percentage
- **Risk Level**: Visual indicator (🟢🟡🔴)
- **Minimum**: Lowest investment amount
- **Users**: Number of active investors
- **Actions**: Quick invest or details buttons

---

## Success Metrics

### Discovery Engagement
- Time spent browsing
- Filter usage patterns
- Details view rate
- Watchlist additions

### Conversion
- Quick Invest usage vs full mandate flow
- Filter-to-invest rate
- Compare-to-invest rate
- NL query success rate

### Bot Performance
- Most viewed bots
- Most invested bots
- Filter popularity
- User preference patterns

---

## Message Templates

### Main Discovery View
```
🔍 Top Trading Strategies

Filter by:
[🏆 Top Gainers] [🛡️ Conservative] [⚡ Aggressive]
[📈 Long-term] [⏱️ Short-term]

---

1. 🥇 Conservative DCA Bot
   APY: 12.5% | Risk: Low 🟢
   Min: $50 | 1,234 users
   [Quick Invest] [Details]

2. 🥈 Grid Trading Pro
   APY: 18.3% | Risk: Medium 🟡
   Min: $100 | 856 users
   [Quick Invest] [Details]

3. 🥉 Arbitrage Master
   APY: 24.7% | Risk: High 🔴
   Min: $200 | 432 users
   [Quick Invest] [Details]

[Load More] [Compare Selected]
```

### Bot Detail
```
🛡️ Conservative DCA Bot

Strategy: Dollar-cost averaging
Risk: Low 🟢 | Min: $50

Performance:
• 30d: +12.5%
• 90d: +38.7%
• All-time: +127.3%

Risk Metrics:
• Max Drawdown: 3.2%
• Sharpe Ratio: 2.8
• Win Rate: 78%

Active Users: 1,234
Total Value Locked: $2.3M

[Quick Invest] [Add to Watchlist]
[Compare with Others] [View Strategy]
[← Back to Discovery]
```

### Quick Invest
```
Quick Invest: Conservative DCA Bot

✅ Optimal settings pre-configured!

Amount:
Available: 1,245.50 USDC
Recommended: $100-500

[$100] [$250] [$500] [Custom]

Duration:
[1 Week] [1 Month] [Custom]

Risk: Moderate 🟡 (Recommended)
[Change Risk Level]

[← Back] [Continue to Review]
```