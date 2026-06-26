import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Zarix AgentOS — AI Workforce Operating System",
  description:
    "Deploy intelligent AI employees that collaborate, build, automate and operate your business.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-neutral-950 text-neutral-100 antialiased">
        {children}
      </body>
    </html>
  );
}
