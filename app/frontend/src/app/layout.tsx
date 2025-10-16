import type { Metadata } from "next";
import "./globals.css";
import { PwaRegister } from "@/components/pwa-register";

export const metadata: Metadata = {
  title: "QR Label Studio",
  description: "Create, print and share delightful QR labels.",
  manifest: "/manifest.json",
  icons: [{ rel: "icon", url: "/icons/icon.svg" }],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="min-h-full">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-950">
        <PwaRegister />
        <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-4 pb-16 pt-8">
          {children}
        </main>
      </body>
    </html>
  );
}
