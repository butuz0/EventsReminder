import type {Metadata} from "next";
import React from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: "KPI Notify",
  description: "Use KPI Notify for planning events for you and your team",
};

export default function RootLayout({children,}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
    <body>
      {children}
    </body>
    </html>
  );
}
