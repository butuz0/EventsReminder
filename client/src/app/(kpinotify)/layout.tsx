import React from "react";
import LeftNavbar from "@/components/shared/navbar/LeftNavbar";
import TopNavbar from "@/components/shared/navbar/TopNavbar";


export default function AppLayout({children,}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex flex-col w-full h-screen">
      <TopNavbar/>
      <div className="flex flex-row h-full p-4">
        <LeftNavbar/>
        <div className="w-full">
          {children}
        </div>
      </div>
    </div>
  );
}