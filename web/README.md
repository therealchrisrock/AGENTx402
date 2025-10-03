# Agent x402 Web Dashboard

A Next.js companion app for the Agent x402 Telegram trading bot, built with the T3 Stack.

## Tech Stack

- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS v4
- **API:** tRPC for type-safe API calls
- **Wallet:** wagmi + viem + RainbowKit
- **State Management:** TanStack Query (React Query)

## Prerequisites

- Node.js 18+
- npm or pnpm
- WalletConnect Project ID (get from https://cloud.walletconnect.com/)

## Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Setup

Copy the example environment file:

```bash
cp .env.example .env.local
```

Edit `.env.local` and add your WalletConnect Project ID:

```env
NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID=your_project_id_here
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```text
web/
├── src/
│   ├── app/                  # Next.js App Router pages
│   │   ├── layout.tsx        # Root layout with providers
│   │   ├── page.tsx          # Home page
│   │   └── api/              # API routes
│   │       └── trpc/         # tRPC endpoint
│   ├── components/           # React components
│   │   └── providers.tsx     # Root providers (tRPC, wagmi, RainbowKit)
│   ├── lib/                  # Utilities
│   │   ├── wagmi.ts          # Wagmi configuration
│   │   └── trpc/             # tRPC client & server setup
│   ├── server/               # Server-side code
│   │   └── api/              # tRPC routers
│   │       ├── routers/      # Individual routers (agent, mandate)
│   │       ├── root.ts       # Root router
│   │       └── trpc.ts       # tRPC initialization
│   └── styles/               # Global styles
│       └── globals.css       # Tailwind imports & custom CSS
├── public/                   # Static assets
├── .env.example              # Environment variables template
├── .env.local                # Local environment (gitignored)
├── next.config.js            # Next.js configuration
├── tailwind.config.ts        # Tailwind CSS configuration
├── tsconfig.json             # TypeScript configuration
└── package.json              # Dependencies & scripts
```

## Available Scripts

```bash
# Development
npm run dev          # Start dev server (localhost:3000)

# Build
npm run build        # Create production build
npm run start        # Start production server

# Linting & Type Checking
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript compiler
```

## Features

### Current
- ✅ Wallet connection (RainbowKit)
- ✅ tRPC integration with FastAPI backend
- ✅ Basic dashboard UI
- ✅ Responsive design with Tailwind CSS v4

### Planned
- [ ] Deep link authentication from Telegram
- [ ] Agent performance dashboard
- [ ] Mandate management UI
- [ ] Trade history viewer
- [ ] Portfolio analytics
- [ ] Real-time updates via WebSockets

## Integration with FastAPI Backend

The web app communicates with the FastAPI backend via tRPC routers that proxy to REST endpoints:

```typescript
// Example: Fetching user's agents
const { data } = trpc.agent.getUserAgents.useQuery({
  userId: userAddress
});
```

tRPC routers are located in `src/server/api/routers/`:
- `agent.ts` - Agent-related queries
- `mandate.ts` - Mandate management

## Deep Linking

See [Deep Linking Strategy](../docs/deep-linking-strategy.md) for details on Telegram ↔ Web integration.

**Example deep link:**
```text
https://app.agentx402.com/agents/{agent_id}?auth={token}
```

## Deployment

### Vercel (Recommended)

1. Push to GitHub
2. Import project in Vercel
3. Add environment variables
4. Deploy

### Self-Hosted

```bash
npm run build
npm run start
```

## Contributing

1. Create feature branch from `main`
2. Make changes
3. Test locally
4. Open pull request

## License

MIT
