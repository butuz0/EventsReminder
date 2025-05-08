import type {Metadata} from "next";
import React from "react";
import "./globals.css";
import {nunito, sourceSerif} from "@/lib/fonts";

export const metadata: Metadata = {
  title: "KPI Notify",
  description: "Use KPI Notify for planning events for you and your team",
};

export default function RootLayout({children,}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
    <body className={`${sourceSerif.variable} ${nunito.variable}`}>
      {children}
    </body>
    </html>
  );
}
