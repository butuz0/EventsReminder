"use client";

import {useAuthSession} from "@/hooks/useAuthSession";
import {ArrowLeftStartOnRectangleIcon} from "@heroicons/react/24/outline";

export default function LogoutButton() {
  const {logout} = useAuthSession();
  
  return (
    <button
      onClick={logout}
      className="flex h-full w-full flex-row items-center
      justify-start gap-3 rounded-xl bg-gray-100 p-2
      text-left hover:bg-red-100 hover:text-red-700
      hover:cursor-pointer"
    >
      <ArrowLeftStartOnRectangleIcon className="w-8"/>
      <p className="w-full">Logout</p>
    </button>
  );
}
