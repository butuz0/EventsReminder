"use client";

import PageTitle from "@/components/shared/PageTitle";
import FacultiesTable from "@/components/units/FacultiesTable";
import {Tabs, TabsList, TabsTrigger, TabsContent} from "@/components/ui/tabs";
import ProfilesList from "@/components/profiles/ProfilesList";
import Search from "@/components/shared/Search";
import {useSearchParams} from "next/navigation";
import {useMemo, Suspense} from "react";
import LoaderComponent from "@/components/shared/Loader";


function UniversityPageContent() {
  const searchParams = useSearchParams();
  const profilesParams = useMemo(() => ({
    search: searchParams.get("search") || undefined,
    page: Number(searchParams.get("page") || 1),
  }), [searchParams]);
  
  return (
    <div>
      <PageTitle title="Університет"/>
      <Tabs defaultValue="users">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="users">
            Користувачі
          </TabsTrigger>
          <TabsTrigger value="university">
            Університет
          </TabsTrigger>
        </TabsList>
        <TabsContent value="users">
          <div className="mb-4">
            <Search placeholder="Шукати користувача"/>
          </div>
          <Suspense
            fallback={
              <LoaderComponent
                size="lg"
                text="Завантаження користувачів..."
                className="h-3/5"
              />
            }
          >
            <ProfilesList queryParams={profilesParams}/>
          </Suspense>
        </TabsContent>
        <TabsContent value="university">
          <FacultiesTable/>
        </TabsContent>
      </Tabs>
    </div>
  );
}

export default function UniversityPage() {
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
      <UniversityPageContent/>
    </Suspense>
  )
}