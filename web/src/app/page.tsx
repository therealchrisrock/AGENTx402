"use client";

import { ConnectButton } from "@rainbow-me/rainbowkit";
import { useAccount } from "wagmi";
import { trpc } from "~/lib/trpc/client";

export default function HomePage() {
  const { address, isConnected } = useAccount();

  // Example tRPC query (will return mock data for now)
  const { data: mandatesData } = trpc.mandate.getUserMandates.useQuery(
    { userId: address ?? "" },
    { enabled: !!address }
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-black text-white">
      <nav className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-sm">
        <div className="container mx-auto flex items-center justify-between px-4 py-4">
          <h1 className="text-2xl font-bold">Agent x402</h1>
          <ConnectButton />
        </div>
      </nav>

      <main className="container mx-auto px-4 py-12">
        <div className="mb-12 text-center">
          <h2 className="mb-4 text-4xl font-bold">
            AI-Powered Trading Dashboard
          </h2>
          <p className="text-xl text-gray-400">
            Monitor and manage your autonomous trading agents
          </p>
        </div>

        {!isConnected ? (
          <div className="mx-auto max-w-md rounded-lg border border-gray-800 bg-gray-900/50 p-8 text-center">
            <h3 className="mb-4 text-xl font-semibold">Connect Your Wallet</h3>
            <p className="mb-6 text-gray-400">
              Connect your wallet to view your trading agents and mandates
            </p>
            <ConnectButton />
          </div>
        ) : (
          <div className="space-y-6">
            <div className="rounded-lg border border-gray-800 bg-gray-900/50 p-6">
              <h3 className="mb-4 text-xl font-semibold">Your Wallet</h3>
              <p className="font-mono text-sm text-gray-400">
                {address}
              </p>
            </div>

            <div className="rounded-lg border border-gray-800 bg-gray-900/50 p-6">
              <h3 className="mb-4 text-xl font-semibold">Active Mandates</h3>
              {mandatesData ? (
                <p className="text-gray-400">{mandatesData.message}</p>
              ) : (
                <p className="text-gray-400">Loading mandates...</p>
              )}
            </div>

            <div className="grid gap-6 md:grid-cols-3">
              <div className="rounded-lg border border-gray-800 bg-gray-900/50 p-6">
                <h4 className="mb-2 text-lg font-semibold">Total Agents</h4>
                <p className="text-3xl font-bold text-blue-400">0</p>
              </div>
              <div className="rounded-lg border border-gray-800 bg-gray-900/50 p-6">
                <h4 className="mb-2 text-lg font-semibold">Active Trades</h4>
                <p className="text-3xl font-bold text-green-400">0</p>
              </div>
              <div className="rounded-lg border border-gray-800 bg-gray-900/50 p-6">
                <h4 className="mb-2 text-lg font-semibold">Total Return</h4>
                <p className="text-3xl font-bold text-purple-400">$0.00</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
