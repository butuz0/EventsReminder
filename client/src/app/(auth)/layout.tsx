import Image from "next/image";
import React from "react";


export default function AuthLayout({children}: { children: React.ReactNode }) {
  return (
    <div
      className="flex min-h-screen flex-col items-center
      justify-center bg-gradient-to-br from-blue-50
      via-white to-blue-100 px-4"
    >
      <div
        className="flex w-full max-w-md flex-col items-center gap-4 rounded-xl
        border border-blue-200 bg-white px-10 pt-7 pb-5 shadow-lg">
        <div className="flex items-center gap-4">
          <Image
            src="/images/logo-blue.svg"
            alt="logo"
            width={60}
            height={60}
          />
          <h1 className="text-5xl text-[#4d4dff] font-sourceSerif">
            КПІ <i>Notify</i>
          </h1>
        </div>
        {children}
      </div>
    </div>
  );
}
