import React from "react";
import Link from "next/link";
import NavbarLinks from "@/components/shared/navbar/NavbarLinks";
import {ArrowLeftStartOnRectangleIcon} from "@heroicons/react/24/outline";


export default function LeftNavbar() {
  return (
    <div className="hidden flex-col gap-2 md:w-69 md:flex">
      <NavbarLinks/>
      <div className="h-full rounded-xl bg-gray-100"></div>
      <div>
        <div className="h-12 w-full text-center text-xl">
          <Link
            href={"/logout"}
            className="flex h-full flex-row items-center justify-start  rounded-xl \
            gap-3 bg-gray-100 p-2 hover:bg-red-100 hover:text-red-700"
          >
            <ArrowLeftStartOnRectangleIcon className="w-8"/>
            <p className="w-full text-left">
              Logout
            </p>
          </Link>
        </div>
      </div>
    </div>
  )
}