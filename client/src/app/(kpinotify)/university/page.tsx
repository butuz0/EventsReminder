"use client";

import PageTitle from "@/components/shared/PageTitle";
import FacultiesTable from "@/components/units/FacultiesTable";
import {Tabs, TabsList, TabsTrigger, TabsContent} from "@/components/ui/tabs";
import ProfilesList from "@/components/profiles/ProfilesList";
import Search from "@/components/shared/Search";
import {useSearchParams} from "next/navigation";
import {useMemo} from "react";


export default function UniversityPage() {
  const searchParams = useSearchParams();
  const profilesParams = useMemo(() => ({
    search: searchParams.get("search") || undefined,
    page: Number(searchParams.get("page") || 1),
  }), [searchParams]);
  
  return (
    <div>
      <PageTitle title="Університет"/>
      <Tabs defaultValue="university">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="university">
            Університет
          </TabsTrigger>
          <TabsTrigger value="users">
            Користувачі
          </TabsTrigger>
        </TabsList>
        <TabsContent value="university">
          <FacultiesTable/>
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