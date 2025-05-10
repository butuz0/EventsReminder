import React from "react";
import NavbarLinks from "@/components/shared/navbar/NavbarLinks";
import LogoutButton from "@/components/shared/navbar/LogoutButton";


export default function LeftNavbar() {
  return (
    <div className="hidden flex-col gap-2 md:w-69 md:flex">
      <NavbarLinks/>
      
      <div className="h-full rounded-xl bg-gray-100"></div>
      
      <div className="h-12 w-full text-xl">
        <LogoutButton/>
      </div>
    </div>
  )
}