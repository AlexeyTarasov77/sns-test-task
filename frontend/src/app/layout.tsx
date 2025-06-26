import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { UIHeader } from "@/widgets/header";
import { AuthProvider } from "@/entity/users/context/auth";
import { UsersProvider } from "@/entity/users/context/user";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "sns",
  description: "View notifications from your social networks",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <UsersProvider>
          <AuthProvider>
            <UIHeader />
            {children}
          </AuthProvider>
        </UsersProvider>
      </body>
    </html>
  );
}
