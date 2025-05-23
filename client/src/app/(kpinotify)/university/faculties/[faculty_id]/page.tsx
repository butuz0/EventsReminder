"use client";

import {useGetFacultyDetailsQuery} from "@/lib/redux/slices/units/unitsApiSlice";
import FacultyDetails from "@/components/units/FacultyDetails";
import {Tabs, TabsContent, TabsList, TabsTrigger} from "@/components/ui/tabs";
import ProfilesList from "@/components/profiles/ProfilesList";
import PageTitle from "@/components/shared/PageTitle";
import {useSearchParams} from "next/navigation";
import {useMemo} from "react";
import Search from "@/components/shared/Search";

interface FacultyPageProps {
  params: {
    faculty_id: string
  }
}


export default function FacultyPage({params}: FacultyPageProps) {
  const facultyId = Number(params.faculty_id);
  
  const searchParams = useSearchParams();
  const profilesParams = useMemo(() => ({
    search: searchParams.get("search") || undefined,
    page: Number(searchParams.get("page") || 1),
    department__faculty: facultyId
  }), [searchParams, facultyId]);
  
  const {data, isLoading, isError} = useGetFacultyDetailsQuery(facultyId);
  
  if (isLoading) {
    return <p className="text-center text-xl">Завантаження...</p>;
  }
  
  if (isError || !data) {
    return (
      <p className="text-center text-xl text-red-600">
        Помилка завантаження факультету або факультету не існує.
      </p>
    );
  }
  return (
    <div>
      <PageTitle title={data.faculty_name}/>
      <Tabs defaultValue="faculty">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="faculty">
            Інститут / Факультет
          </TabsTrigger>
          <TabsTrigger value="users">
            Користувачі
          </TabsTrigger>
        </TabsList>
        <TabsContent value="faculty">
          <FacultyDetails departments={data.departments}/>
        </TabsContent>
        <TabsContent value="users">
          <div className="mb-4">
            <Search placeholder="Шукати користувача"/>
          </div>
          <ProfilesList queryParams={profilesParams}/>
        </TabsContent>
      </Tabs>
    </div>
  );
}