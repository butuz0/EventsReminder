import React from "react";
import Link from "next/link";
import NavbarLinks from "@/components/shared/navbar/NavbarLinks";
import {ArrowLeftStartOnRectangleIcon} from "@heroicons/react/24/outline";


export default function LeftNavbar() {
  return (
    <div className="hidden flex-col gap-2 md:flex md:w-69">
      <NavbarLinks/>
      <div className="h-full rounded-xl bg-gray-50"></div>
      <div>
        <div className="h-12 w-full rounded-xl bg-gray-50 text-center text-xl">
          <Link href={"/logout"} className="flex h-full flex-row items-center justify-start gap-3 p-2">
            <ArrowLeftStartOnRectangleIcon className="w-8"/>
            <p className="hidden w-full text-left sm:block">
              Logout
            </p>
          </Link>
        </div>
      </div>
    </div>
  )
}