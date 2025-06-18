"use client";

import DepartmentDetails from "@/components/units/DepartmentDetails";
import {useSearchParams} from "next/navigation";
import {Suspense, useMemo} from "react";
import LoaderComponent from "@/components/shared/Loader";

interface DepartmentDetailsPageProps {
  params: {
    department_id: number
  }
}


function DepartmentDetailsContent({params}: DepartmentDetailsPageProps) {
  const departmentId = params.department_id;
  
  const searchParams = useSearchParams();
  const profilesParams = useMemo(() => ({
    search: searchParams.get("search") || undefined,
    page: Number(searchParams.get("page") || 1),
    department: departmentId
  }), [searchParams, departmentId]);
  
  return (
    <DepartmentDetails departmentId={departmentId} queryParams={profilesParams}/>
  )
}

export default function DepartmentDetailsPage({params}: DepartmentDetailsPageProps) {
  return (
    <Suspense
      fallback={
        <LoaderComponent
          size="lg"
          text="Завантаження користувачів..."
          className="h-3/5"
        />
      }
    >
      <DepartmentDetailsContent params={params}/>
    </Suspense>
  )
}