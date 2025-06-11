"use client";

import {useAuthSession} from "@/hooks/useAuthSession";
import {ArrowLeftStartOnRectangleIcon} from "@heroicons/react/24/outline";


export default function LogoutButton() {
  const {logout} = useAuthSession();
  
  return (
    <button
      onClick={logout}
      className="flex h-full w-full flex-row items-center
      justify-start gap-3 rounded-xl bg-white p-2
      border border-blue-200 text-left
      hover:bg-red-100 hover:text-red-700
      hover:border-red-400 hover:cursor-pointer"
    >
      <ArrowLeftStartOnRectangleIcon className="w-8"/>
      <p className="w-full">Вихід</p>
    </button>
  );
}
