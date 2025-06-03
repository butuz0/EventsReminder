"use client"

import {MagnifyingGlassIcon} from "@heroicons/react/24/outline";
import {useSearchParams, usePathname, useRouter} from "next/navigation";
import React, {useEffect, useState} from "react";
import {useDebouncedCallback} from "use-debounce";

interface SearchProps {
  placeholder?: string
}


export default function Search({placeholder = "Пошук..."}: SearchProps) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const {replace} = useRouter();
  
  const [input, setInput] = useState(searchParams.get("search") ?? "");
  
  useEffect(() => {
    setInput(searchParams.get("search") ?? "");
  }, [searchParams]);
  
  const updateQueryParams = useDebouncedCallback((term: string) => {
    const params = new URLSearchParams(searchParams);
    if (term) {
      params.set("search", term);
      params.delete("page");
    } else {
      params.delete("search");
    }
    replace(`${pathname}?${params.toString()}`);
  }, 500);
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const term = e.target.value;
    setInput(term);
    updateQueryParams(term);
  };
  
  return (
    <div className="relative w-full">
      <input
        type="text"
        className="w-full rounded-md border border-gray-200 shadow-sm
        bg-white pl-10 pr-3 py-2 text-sm placeholder:text-gray-600
        focus:outline-none focus:border-blue-500"
        placeholder={placeholder}
        value={input}
        onChange={handleChange}
      />
      <MagnifyingGlassIcon
        className="absolute left-3 top-1/2 w-5
        -translate-y-1/2 text-gray-400"
      />
    </div>
  );
}
