"use client";

import Link from "next/link";
import clsx from "clsx";
import {useGetAllFacultiesQuery} from "@/lib/redux/slices/units/unitsApiSlice";


export default function FacultiesTable() {
  const {data, isLoading} = useGetAllFacultiesQuery();
  
  if (isLoading) {
    return (
      <p className="w-full text-center text-5xl">
        Завантаження
      </p>
    )
  }
  
  const faculties = data?.faculties.results;
  
  return (
    <div className="rounded-xl bg-gray-100 p-2 shadow-lg border border-gray-200">
      <div className="grid rounded-t-xl px-4 py-5 font-semibold grid-cols-[1fr_3fr_1fr]">
        <div>Інститут / Факультет</div>
        <div>Повна назва</div>
        <div>Користувачі</div>
      </div>
      
      <div className="divide-y-3 divide-gray-100">
        {faculties?.map((faculty, i) => (
          <Link
            key={faculty.id}
            href={`/teams/invitations/create/faculties/${faculty.id}/`}
            className={clsx(
              "grid items-center bg-white px-4 py-5 grid-cols-[1fr_3fr_1fr] " +
              "hover:bg-gray-200 transition-colors",
              i === 0 && "rounded-t-md",
              i === faculties.length - 1 && "rounded-b-md"
            )}
          >
            <div>{faculty.faculty_abbreviation}</div>
            <div className="pr-2">{faculty.faculty_name}</div>
            <div>{faculty.num_employees}</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
