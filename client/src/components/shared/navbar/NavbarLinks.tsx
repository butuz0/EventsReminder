"use client";

import {LeftNavbarLinks} from "@/constants";
import {usePathname} from "next/navigation";
import {clsx} from "clsx";
import Link from "next/link";
import React from "react";


export default function NavbarLinks() {
  const pathname = usePathname();
  
  return (
    <div className="flex flex-col gap-2">
      {LeftNavbarLinks.map((link => {
        const LinkIcon = link.icon;
        return (
          <div key={link.label} className="h-14 w-full text-center text-xl">
            <Link
              href={link.href}
              className={clsx(
                "flex h-full flex-row items-center justify-start gap-3 p-2 " +
                "bg-gray-100 rounded-xl hover:bg-sky-100 hover:text-blue-600",
                {"bg-sky-100 text-blue-600": pathname === link.href},
              )}>
              <LinkIcon className="w-8"/>
              <p className="w-full text-left">
                {link.label}
              </p>
            </Link>
          </div>
        )
      }))}
    </div>
  )
}