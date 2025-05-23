"use client";

import DepartmentDetails from "@/components/units/DepartmentDetails";
import {useSearchParams} from "next/navigation";
import {useMemo} from "react";

interface DepartmentDetailsPageProps {
  params: {
    department_id: number
  }
}


export default function DepartmentDetailsPage({params}: DepartmentDetailsPageProps) {
  const departmentId = params.department_id;
  
  const searchParams = useSearchParams();
  const profilesParams = useMemo(() => ({
    search: searchParams.get("search") || undefined,
    page: Number(searchParams.get("page") || 1),
    department: departmentId
  }), [searchParams, departmentId]);
  
  return (
    <div>
      <DepartmentDetails departmentId={departmentId} queryParams={profilesParams}/>
    </div>
  )
}