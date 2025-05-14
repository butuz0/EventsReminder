"use client";

import {useGetFacultyDetailsQuery} from "@/lib/redux/slices/units/unitsApiSlice";
import FacultyDetails from "@/components/units/FacultyDetails";
import {Tabs, TabsContent, TabsList, TabsTrigger} from "@/components/ui/tabs";
import ProfilesList from "@/components/profiles/ProfilesList";
import PageTitle from "@/components/shared/PageTitle";

interface FacultyPageProps {
  params: {
    faculty_id: string
  }
}


export default function FacultyPage({params}: FacultyPageProps) {
  const facultyId = Number(params.faculty_id);
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
          <ProfilesList queryParams={{department__faculty: facultyId}}/>
        </TabsContent>
      </Tabs>
    </div>
  );
}