"use client";

import Link from "next/link";
import clsx from "clsx";
import {Department} from "@/types";

interface FacultyDetailsProps {
  departments: Department[];
}


export default function FacultyDetails({departments}: FacultyDetailsProps) {
  return (
    <div>
      <div className="rounded-xl bg-gray-100 p-2 shadow-lg border border-gray-200">
        <div className="grid rounded-t-xl px-4 py-5 font-semibold grid-cols-[1fr_4fr_1fr]">
          <div>Кафедра</div>
          <div>Повна назва</div>
          <div>Користувачі</div>
        </div>
        
        <div className="divide-y-3 divide-gray-100">
          {departments?.map((department, i) => (
            <Link
              key={department.id}
              href={`/university/departments/${department.id}/`}
              className={clsx(
                "grid items-center bg-white px-4 py-5 grid-cols-[1fr_4fr_1fr] " +
                "hover:bg-gray-200 transition-colors",
                i === 0 && "rounded-t-md",
                i === departments.length - 1 && "rounded-b-md"
              )}
            >
              <div>{department.department_abbreviation}</div>
              <div>{department.department_name}</div>
              <div>{department.num_employees}</div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}