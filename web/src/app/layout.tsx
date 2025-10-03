import type { Metadata } from "next";
import { Providers } from "~/components/providers";
import "~/styles/globals.css";

export const metadata: Metadata = {
  title: "Agent x402 - AI Trading Dashboard",
  description: "Monitor and manage your autonomous trading agents",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
