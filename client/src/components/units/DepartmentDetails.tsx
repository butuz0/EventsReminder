"use client";

import PageTitle from "@/components/shared/PageTitle";
import {useGetDepartmentDetailsQuery} from "@/lib/redux/slices/units/unitsApiSlice";
import ProfilesList from "@/components/profiles/ProfilesList";
import Search from "@/components/shared/Search";

interface DepartmentDetailsProps {
  departmentId: number,
  queryParams?: Record<string, any>
}


export default function DepartmentDetails({departmentId, queryParams}: DepartmentDetailsProps) {
  const {data, isLoading} = useGetDepartmentDetailsQuery(departmentId);
  const department = data?.department;
  
  return (
    <div>
      <PageTitle title={department?.department_name}/>
      <div className="mb-4">
        <Search placeholder="Шукати користувача"/>
      </div>
      <ProfilesList queryParams={queryParams}/>
    </div>
  )
}