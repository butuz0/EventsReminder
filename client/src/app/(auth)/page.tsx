import Link from "next/link";
import Image from "next/image";
import React from "react";

export default function Home() {
  return (
    <div
      className="flex min-h-screen flex-col items-center
      justify-center bg-gradient-to-br from-blue-50
      via-white to-blue-100 px-4"
    >
      <div
        className="flex flex-col items-center gap-8 rounded-2xl
        border border-blue-200 bg-white p-10 shadow-lg
        max-w-md w-full"
      >
        <div className="flex items-center gap-4">
          <Image
            src="/images/logo-blue.svg"
            alt="logo"
            width={60}
            height={60}
          />
          <h1 className="text-5xl text-blue-800 font-sourceSerif">
            КПІ <i>Notify</i>
          </h1>
        </div>
        
        <p className="text-center text-lg text-gray-600">
          Ласкаво просимо! Керуйте подіями та нагадуваннями у своєму університетському житті легко і зручно.
        </p>
        
        <div className="flex w-full flex-col gap-3">
          <Link
            href="/register"
            className="w-full rounded-lg bg-blue-600 px-6 py-3
            text-center text-lg font-medium text-white shadow-md
            transition hover:bg-blue-700"
          >
            Зареєструватись
          </Link>
          
          <p className="text-center text-sm text-gray-500">Вже маєте акаунт?</p>
          
          <Link
            href="/login"
            className="w-full rounded-lg border border-blue-600 px-6 py-3 text-center text-lg font-medium text-blue-600 transition hover:bg-blue-50"
          >
            Увійти
          </Link>
        </div>
      </div>
    </div>
  );
}
