"use client";

import PageTitle from "@/components/shared/PageTitle";
import {useGetDepartmentDetailsQuery} from "@/lib/redux/slices/units/unitsApiSlice";
import ProfilesList from "@/components/profiles/ProfilesList";

interface DepartmentDetailsProps {
  departmentId: number
}


export default function DepartmentDetails({departmentId}: DepartmentDetailsProps) {
  const {data, isLoading} = useGetDepartmentDetailsQuery(departmentId);
  const department = data?.department;
  
  return (
    <div>
      <PageTitle title={department?.department_name}/>
      <ProfilesList queryParams={{department: departmentId}}/>
    </div>
  )
}