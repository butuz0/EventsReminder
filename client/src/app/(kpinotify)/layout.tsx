import React from "react";
import LeftNavbar from "@/components/shared/navbar/LeftNavbar";
import TopNavbar from "@/components/shared/navbar/TopNavbar";
import ProtectedRoute from "@/components/shared/ProtectedRoute";


export default function AppLayout({children,}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ProtectedRoute>
      <div
        className="flex min-h-screen w-full flex-col
      bg-gradient-to-br from-blue-50
      via-white to-blue-100"
      >
        <TopNavbar/>
        <div className="flex h-full flex-row p-4">
          <LeftNavbar/>
          <div className="w-full px-5">
            {children}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}