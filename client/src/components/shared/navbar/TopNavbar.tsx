import Image from "next/image";
import React from "react";
import Link from "next/link";


export default function TopNavbar() {
  return (
    <div className="h-20 bg-[#4d4dff] px-2 font-sourceSerif">
      <Link href="/home" className="h-full flex flex-row items-center gap-3">
        <Image
          src="images/logo.svg"
          alt="logo"
          width={60}
          height={60}
          className=""
        />
        <p className="text-4xl text-white">
          КПІ <i>Notify</i>
        </p>
      </Link>
    </div>
  )
}