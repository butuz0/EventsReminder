"use client";

import Link from "next/link";
import clsx from "clsx";
import {useGetFacultyDetailsQuery} from "@/lib/redux/slices/units/unitsApiSlice";
import PageTitle from "@/components/shared/PageTitle";


interface FacultyDetailsProps {
  facultyId: number;
}


export default function FacultyDetails({facultyId}: FacultyDetailsProps) {
  const {data, isLoading} = useGetFacultyDetailsQuery(facultyId);
  
  if (isLoading) {
    return (
      <p className="w-full text-center text-4xl">
        Завантаження
      </p>
    )
  }
  
  if (data?.departments.length === 0) {
    return (
      <p className="w-full text-center text-4xl">
        Факультету із id={facultyId} не існує.
      </p>
    )
  }
  
  const departments = data?.departments;
  
  return (
    <div>
      <PageTitle title={data?.faculty_name}/>
      
      <div className="rounded-xl bg-gray-100 p-2 shadow-lg">
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